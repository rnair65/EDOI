import pandas as pd
import oracledb

# Establish the database connection
try:
    connection = oracledb.connect(
        config_dir="Wallet_EDOI",
        user="admin",
        password="ASUEDOIndex25",
        dsn="edoi_low",
        wallet_location="Wallet_EDOI",
        wallet_password="ASUEDOIndex25"
    )
    print("Database connection established.")
except oracledb.DatabaseError as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Read the CSV file into a DataFrame
csv_file_path = "live_data/fortune_100_best_companies_to_work_for_2024.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)
print("CSV data loaded successfully.")
print(df.head())

# Create a cursor
cursor = connection.cursor()

# Map pandas datatypes to Oracle datatypes
def get_oracle_type(pandas_dtype):
    if pd.api.types.is_integer_dtype(pandas_dtype):
        return "NUMBER"
    elif pd.api.types.is_float_dtype(pandas_dtype):
        return "NUMBER"
    elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
        return "DATE"
    else:
        return "VARCHAR2(4000)"  # Default to VARCHAR2 with large size

# Generate CREATE TABLE statement dynamically
table_name = "edoi_database"  # Change to your desired table name
columns_def = []

for col_name, dtype in df.dtypes.items():
    oracle_type = get_oracle_type(dtype)
    # Replace spaces and special characters in column names
    clean_col_name = col_name.replace(" ", "_").replace("-", "_")
    columns_def.append(f'"{clean_col_name}" {oracle_type}')

create_table_query = f"""
CREATE TABLE {table_name} (
    {", ".join(columns_def)}
)
"""

try:
    cursor.execute(create_table_query)
    print(f"Table {table_name} created successfully.")
except oracledb.DatabaseError as e:
    error = e.args[0]
    if error.code == 955:  # ORA-00955: name is already used by an existing object
        print("Table already exists. Proceeding with data upload.")
    else:
        print(f"Error creating table: {e}")
        print(f"Query that failed: {create_table_query}")
        cursor.close()
        connection.close()
        exit()

# Upload data to the new table
try:
    # First prepare the INSERT statement with proper column names
    clean_col_names = [col.replace(" ", "_").replace("-", "_") for col in df.columns]
    columns = ", ".join([f'"{col}"' for col in clean_col_names])
    placeholders = ", ".join([":"+str(i+1) for i in range(len(df.columns))])
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Batch insert data
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size].values.tolist()
        cursor.executemany(insert_query, batch)
        connection.commit()
        print(f"Inserted records {i} to {min(i+batch_size, len(df))}.")
    
    print("All data uploaded successfully.")
    
except oracledb.DatabaseError as e:
    print(f"Error inserting data: {e}")
    print(f"Query that failed: {insert_query}")
    connection.rollback()

# Close cursor and connection
cursor.close()
connection.close()
print("Database connection closed.")