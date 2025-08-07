import pandas as pd
import smtplib
from email.mime.text import MIMEText
import os

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "adekeyedamilarelekan@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = "r**j **** v**u ****"  # Replace with your Gmail App Password

# Path to your CSV file
csv_path = "C:/Users/Aorus15/Desktop/PropertyVisualizer/generated_emails.csv"

# Read the CSV file
try:
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} emails from {csv_path}")
except Exception as e:
    print(f"Error reading CSV file: {str(e)}")
    exit()

# Verify the required columns
required_columns = ["Company Name", "Email Address", "Generated Email"]
if not all(col in df.columns for col in required_columns):
    print(f"CSV file must contain the following columns: {required_columns}")
    exit()

# Function to send an email


def send_email(to_email, subject, body, from_email, password):
    try:
        # Create a MIMEText object
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(from_email, password)  # Login with your credentials
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")


# Select the first row for testing (no actual leads)
if not df.empty:
    test_row = df.iloc[0]  # Use the first row for testing
    test_company = test_row["Company Name"]
    test_email_content = test_row["Generated Email"]
    test_subject = f"Test Collaboration Proposal for {test_company}"

    # Send test email to team@propertyvisualizer.com, adekeyedamilarelekan@gmail.com
    send_email(
        # to_email="adekeyedamilarelekan@gmail.com",      # I tested with my email first and i was sure that it arrived in my inbox, so i sent a test email to team@propertyvisualizer.com
        to_email="team@propertyvisualizer.com",
        subject=test_subject,
        body=test_email_content,
        from_email=SENDER_EMAIL,
        password=SENDER_PASSWORD
    )
else:
    print("No data found in the CSV file to test.")

# Commented-out block to send emails to all leads (DO NOT UNCOMMENT TO RUN)
'''
# Send emails to all leads (commented out to avoid sending to actual leads)
for index, row in df.iterrows():
    company_name = row["Company Name"]
    email_address = row["Email Address"]
    email_content = row["Generated Email"]
    subject = f"Collaboration Proposal for {company_name}"

    print(f"Preparing to send email to {company_name} ({email_address})")
    send_email(
        to_email=email_address,
        subject=subject,
        body=email_content,
        from_email=SENDER_EMAIL,
        password=SENDER_PASSWORD
    )
    # Add a delay to avoid rate limiting (e.g., 2 seconds)
    time.sleep(2)

print("Email sending process completed for all leads.")
'''

# Keep the script running for review
input("Press Enter to exit...")
