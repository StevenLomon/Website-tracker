import streamlit as st
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Function to fetch website content
def fetch_site_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to compare content
def compare_content(old_content, new_content):
    return old_content != new_content

# Function to send email
def send_email(recipient_email, subject, body):
    sender_email = "your_email@example.com"  # Enter your email
    sender_password = "your_email_password"  # Enter your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Use your SMTP server details
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Streamlit UI
st.title("Website Change Detector")
url = st.text_input("Enter the website URL:")
email = st.text_input("Enter your email address:")
check_interval = st.number_input("Check interval in seconds:", min_value=30, value=60)

if st.button("Start Monitoring"):
    original_content = fetch_site_content(url)
    if original_content:
        st.success("Monitoring started. You will receive an email if a change is detected.")
        while True:
            time.sleep(check_interval)
            new_content = fetch_site_content(url)
            if compare_content(original_content, new_content):
                send_email(email, "Website Change Detected", f"A change was detected on {url}")
                original_content = new_content  # Update the original content to the new content after change detection
    else:
        st.error("Failed to fetch website content. Please check the URL and try again.")
