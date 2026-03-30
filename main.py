import os
import requests
import boto3

# API URL for Gold Price
gold_api_url = "https://www.goldapi.io/api/XAU/INR"

# API KEY (from goldapi.io)
gold_api_key = os.getenv("GOLD_API_KEY")

# SNS Topic ARN (AWS)
sns_topic_arn = os.getenv("SNS_TOPIC_ARN")

# Call Gold API
response = requests.get(
    gold_api_url,
    headers={
        "x-access-token": gold_api_key,
        "Content-Type": "application/json"
    }
)

data = response.json()
price = data.get("price")

# Message to send
message = f"Today's Gold Price: ₹{price}"

# Publish to SNS
sns = boto3.client("sns")
sns.publish(
    TopicArn=sns_topic_arn,
    Message=message,
    Subject="Gold Price Alert"
)

print("Notification sent successfully.")