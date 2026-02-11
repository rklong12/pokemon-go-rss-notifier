Pokémon GO RSS Notifier

An AWS Lambda–based RSS monitoring service that checks for new Pokémon GO blog posts and sends email notifications when updates are detected.

This project uses:

AWS Lambda (Python 3.12)

Amazon SES (email notifications)

AWS Systems Manager Parameter Store (SSM) (state tracking)

Amazon EventBridge (scheduled automation)

Feedparser (RSS parsing)

📌 Overview

This service periodically checks an RSS feed for new entries.

It tracks the number of previously seen posts using SSM Parameter Store.

If the feed contains new entries since the last check:

An email notification is sent via SES

The stored counter is updated

Execution logs are written to CloudWatch

The function is designed to run automatically on a schedule (e.g., every 15 minutes).

🏗 Architecture

EventBridge (cron schedule)
→ Lambda function
→ Fetch RSS feed
→ Compare entry count with SSM parameter
→ If new posts detected → Send email via SES
→ Update SSM parameter
