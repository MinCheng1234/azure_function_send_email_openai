import os
import logging
import json
import smtplib
from email.mime.text import MIMEText
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func

app = func.FunctionApp()

# Set up Key Vault client
key_vault_url = os.getenv("KEY_VAULT_URL")  # Key Vault URL from environment variables
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

@app.function_name(name="SendEmail")
@app.route(route="send-email", methods=["POST"])
def send_email(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing an HTTP request to send an email.")

    try:
        # Retrieve secrets from Azure Key Vault
        email_username = client.get_secret("EmailUsername").value
        email_password = client.get_secret("EmailPassword").value

        # Parse request parameters for email content
        req_body = req.get_json()
        to_email = req_body.get("to_email")
        subject = req_body.get("subject", "Test Email")
        body = req_body.get("body", "This is a test email sent from Azure Function.")

        # Validate required parameters
        if not to_email:
            return func.HttpResponse(
                json.dumps({"error": "Missing required parameter: 'to_email'"}),
                status_code=400,
                mimetype="application/json"
            )

        # Create the email message
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email_username
        msg["To"] = to_email

        # Send the email using SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_username, email_password)
            server.sendmail(email_username, to_email, msg.as_string())

        return func.HttpResponse(
            json.dumps({"message": "Email sent successfully!"}),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
