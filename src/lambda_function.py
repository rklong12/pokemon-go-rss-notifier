import os
import boto3
import feedparser
from botocore.exceptions import ClientError

# Environment variables
RSS_URL = os.environ['RSS_URL']
EMAIL_FROM = os.environ['EMAIL_FROM']
EMAIL_TO = os.environ['EMAIL_TO']
SSM_PARAM = os.environ['SSM_PARAM']

# AWS clients
ssm = boto3.client('ssm')
ses = boto3.client('ses')

# Helper functions
def get_last_post_id():
    try:
        response = ssm.get_parameter(Name=SSM_PARAM)
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        return None

def set_last_post_id(post_id):
    ssm.put_parameter(
        Name=SSM_PARAM,
        Value=str(post_id),
        Type='String',
        Overwrite=True
    )
    print(f"Updated last_post_id to: {post_id}")

def send_email(subject, body, link, published):
    try:
        ses.send_email(
            Source=EMAIL_FROM,
            Destination={'ToAddresses': [EMAIL_TO]},
            Message={
                'Subject': {'Data': f"New Pokémon GO Update: {subject}"},
                'Body': {'Text': {'Data': f"{body}\nLink: {link}\nPublished: {published}"}}
            }
        )
        print(f"Email sent for post: {subject}")
    except ClientError as e:
        print(f"Failed to send email: {e}")

# Lambda handler
def lambda_handler(event, context):
    print("Fetching RSS feed...")
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No entries found in feed.")
        return

    last_post_id = get_last_post_id()
    print(f"Last post ID: {last_post_id}")

    new_posts_found = False

    for entry in feed.entries:
        # Use id, or fallback to link or published timestamp
        post_id = entry.get('id') or entry.get('link') or entry.get('published')
        if post_id is None:
            print("Skipping entry with no unique identifier.")
            continue

        # Send email if this post is new
        if str(post_id) != str(last_post_id):
            print(f"Sending email for post id: {post_id}")
            send_email(entry.get('title'), entry.get('summary'), entry.get('link'), entry.get('published'))
            set_last_post_id(post_id)
            new_posts_found = True
        else:
            print(f"Already sent post id: {post_id}")

    if not new_posts_found:
        print("No new updates.")
