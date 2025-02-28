from openai import OpenAI
client = OpenAI()
import pandas as pd

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Find every EIN of the following companies: "
#         }
#     ]
# )

# print(completion.choices[0].message)
df = pd.read_csv('static_data/just_capitals_just_100_2024.csv')

# Create a single request to ChatGPT for all company names
company_names = ', '.join(df['COMPANY'].tolist())
prompt = f"Find the US legal name for the following companies: {company_names}."

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)
print(response.choices[0].message)

# # Extract the EINs from the response
# response_text = response['choices'][0]['message']['content']
# ein_dict = {}
# for line in response_text.split('\n'):
#     parts = line.split(':')
#     if len(parts) == 2:
#         company_name, ein = parts
#         ein_dict[company_name.strip()] = ein.strip()

# # Map the EINs to the DataFrame
# df['EIN'] = df['COMPANY'].map(ein_dict)

# print(df)