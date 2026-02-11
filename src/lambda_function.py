import boto3
import feedparser
import os

ses = boto3.client("ses")
ssm = boto3.client("ssm")

RSS_URL = os.environ["RSS_URL"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
SSM_PARAM = os.environ["SSM_PARAM"]


def get_last_post_id():
    return ssm.get_parameter(Name=SSM_PARAM)["Parameter"]["Value"]


def set_last_post_id(post_id):
    ssm.put_parameter(
        Name=SSM_PARAM,
        Value=post_id,
        Type="String",
        Overwrite=True
    )


def send_email(title, summary, link, published):
    ses.send_email(
        Source=EMAIL_FROM,
        Destination={"ToAddresses": [EMAIL_TO]},
        Message={
            "Subject": {"Data": f"New Pokémon GO Update: {title}"},
            "Body": {
                "Text": {
                    "Data": f"{title}\n\n{summary}\n\nRead more: {link}\n\nPublished: {published}"
                }
            },
        },
    )


def lambda_handler(event, context):
    feed = feedparser.parse(RSS_URL)
    last_post_id = get_last_post_id()

    new_entries = []

    for entry in feed.entries:
        if entry.id > last_post_id:
            new_entries.append(entry)

    if not new_entries:
        print("No new updates.")
        return

    # Process oldest first
    new_entries.sort(key=lambda e: e.id)

    for entry in new_entries:
        send_email(
            entry.title,
            entry.summary,
            entry.link,
            entry.published
        )
        set_last_post_id(entry.id)

    print(f"Processed {len(new_entries)} new updates.")
