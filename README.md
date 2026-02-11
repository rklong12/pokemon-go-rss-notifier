Pokémon GO RSS Email Notifier (Serverless)

A fully serverless notification system that monitors Pokémon GO news and sends email updates automatically.

Architecture

EventBridge (scheduled trigger)
→ AWS Lambda (Python 3.12)
→ RSS Feed (pokemonblog.com)
→ AWS SES (email delivery)
→ AWS SSM Parameter Store (state tracking)

Features

Serverless architecture (no servers to manage)

Automatic scheduled execution

State persistence using AWS Parameter Store

Duplicate prevention using last_post_id tracking

Fully automated email notifications

Free-tier compatible

Technologies Used

AWS Lambda

Amazon EventBridge

Amazon SES

AWS Systems Manager (Parameter Store)

Python 3.12

feedparser

How It Works

EventBridge triggers Lambda every 15 minutes.

Lambda fetches the RSS feed.

It compares each post against the stored last_post_id.

If a new post is found:

Sends an email via SES

Updates last_post_id in SSM

Prevents duplicate notifications automatically.

Environment Variables
RSS_URL
EMAIL_FROM
EMAIL_TO
SSM_PARAM

IAM Permissions Required

ssm:GetParameter

ssm:PutParameter

ses:SendEmail

Deployment Steps

Install dependencies:

pip install -r requirements.txt -t .


Zip contents:

zip -r deployment_package.zip .


Upload to AWS Lambda.

Configure environment variables.

Create EventBridge rule:

rate(15 minutes)

Future Improvements

Discord webhook support

SMS notifications via SNS

Multiple feed monitoring

HTML-formatted email

Dockerized Lambda deployment