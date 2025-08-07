import pandas as pd
import openai
from openai import OpenAI
import os

# Set your OpenAI API key
# Replace 'your-api-key-here' with your actual OpenAI API key
openai_api_key = 'sk-proj-z-OrQzjwd5WzBeh8es-MnOEVypX0sjZ9V1gBiwB2YValTcMgYUKARwOKWAns6XcDw7vaMdMA'
if not openai_api_key:
    raise ValueError("Please set your OpenAI API key in the script.")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Path to your CSV file
csv_path = "C:/Users/Aorus15/Desktop/PropertyVisualizer/leads.csv"

# Read the CSV file
try:
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} leads from {csv_path}")
except Exception as e:
    print(f"Error reading CSV file: {str(e)}")
    exit()

# Verify the required columns
required_columns = ["Company Name", "Email"]
if not all(col in df.columns for col in required_columns):
    print(f"CSV file must contain the following columns: {required_columns}")
    exit()

# Function to generate a personalized email using OpenAI
def generate_personalized_email(company_name, email):
    # Define the prompt for OpenAI
    prompt = (
        f"Write a professional and polite email to a real estate company (Immobilienmakler) in Berlin, Germany. "
        f"The email should be in German, addressed to the company '{company_name}', and sent from a fictional sender named 'Damilare Adekeye' "
        f"from a company called 'PropertyVisualizer'. The purpose of the email is to propose a potential collaboration "
        f"for property listings and client referrals. Keep the tone friendly and professional, and the email should be concise (150-200 words). "
        f"Include a subject line and a proper email signature. The sender email is Damilare@PropertyVisualizer.com, +2348163180829"
        f"Note: Do no make mistakes or regenerate duplicate sentences for each email, as it has to be professional in nature."
    )

    try:
        # Call the OpenAI API to generate the email
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a professional email writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        # Extract the generated email text
        email_content = response.choices[0].message.content.strip()
        return email_content

    except Exception as e:
        print(f"Error generating email for {company_name}: {str(e)}")
        return None

# Generate emails for each company
emails = []
for index, row in df.iterrows():
    company_name = row["Company Name"]
    email_address = row["Email"]
    print(f"Generating email for: {company_name} ({email_address})")

    # Generate the email
    email_content = generate_personalized_email(company_name, email_address)
    if email_content:
        emails.append({
            "Company Name": company_name,
            "Email Address": email_address,
            "Generated Email": email_content
        })
        print(f"✓ Email generated for {company_name}")
    else:
        print(f"⨯ Failed to generate email for {company_name}")

# Save the generated emails to a new CSV file
if emails:
    email_df = pd.DataFrame(emails)
    output_csv_path = "C:/Users/Aorus15/Desktop/PropertyVisualizer/generated_emails.csv"
    email_df.to_csv(output_csv_path, index=False)
    print(f"Saved {len(emails)} generated emails to {output_csv_path}")
else:
    print("No emails were generated.")

# Optional: Display the first few emails for review
if emails:
    print("\nSample of generated emails:")
    for i, email in enumerate(emails[:3]):  # Show first 3 emails
        print(f"\nEmail {i+1}:")
        print(f"Company: {email['Company Name']}")
        print(f"Email Address: {email['Email Address']}")
        print(f"Generated Email:\n{email['Generated Email']}\n")