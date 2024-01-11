# Slack Bot with JIRA Integration

## Overview

This project involves developing a Slack bot integrated with JIRA, designed to streamline task management and enhance team collaboration within Slack. The bot not only interacts with users in Slack but also logs activities in JIRA, offering a blend of immediate communication and efficient project tracking.

## Key Responsibilities and Features

### Slackbot Development

The Slackbot is engineered with the following capabilities:

1. **Identity Logging**: On initiating a chat, the bot logs the identity of the user.
2. **Interactive Questionnaire**:
   - The bot asks a series of 10 yes/no questions.
   - Each 'yes' response is scored, and a total score is tallied.
   - Based on the total score, the bot matches the user to one of five predefined categories.
   - It then provides guidance based on the matched category.
   
### JIRA Integration

- The bot is equipped to log a ticket in JIRA with details of the user’s responses and the final category they fall into. This feature aids in tracking user responses and categorization for future reference and analysis.

### AWS Lambda Deployment

- The bot is optimized for deployment on AWS Lambda, ensuring efficiency and scalability. This includes handling serverless operations and being able to manage varying loads effectively.

### Testing and Documentation

- Extensive testing is conducted to ensure the bot's reliability and accuracy in user interaction and data logging.
- Detailed documentation is provided, covering the bot's functionality, setup process, and maintenance guidelines. This documentation serves as a valuable resource for future reference and modifications.

## Prerequisites

- Python 3.11
- An AWS account
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

### Python Dependencies

- [boto3](https://pypi.org/project/boto3/) for AWS SDK.
- [slack-bolt](https://pypi.org/project/slack-bolt/) for building Slack apps.
- [jira](https://pypi.org/project/jira/) for JIRA REST API interactions.

## AWS Integration

### 1. AWS Credentials Setup

Configure your AWS credentials in `./aws/credentials`:

```text
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY
aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY
```

### 2. Secrets Management

Create a secret in AWS Secrets Manager with the following keys:
- `SLACK_BOT_TOKEN`: Your Slack bot token.
- `SLACK_SIGNING_SECRET`: Slack signing secret for verification.
- `SLACK_SLASH_COMMAND`: Command trigger name for Slack. (Example: `/security-test`)
- `JIRA_API_TOKEN`: JIRA API access token.
- `JIRA_USER`: JIRA username.
- `JIRA_PROJECT_KEY`: Key identifier for your JIRA project.

### 3. AWS Lambda Function Layer

Prepare Layer to deploy:

```
mkdir -p layer/python/lib/python3.11/site-packages

pip install -r requirements.txt -t layer/python/lib/python3.11/site-packages
```

### 4. AWS Lambda Deployment

Deploy the bot on AWS Lambda:

```bash
export SECRET_ARN="ARN_of_your_secret"

sam build

sam deploy --parameter-overrides SecretArn=$SECRET_ARN StageName=prod
```

Use `--guided` parameter to control more deployment details:

```bash
sam deploy --guided --parameter-overrides ...
```

### 5. Slack Bot Setup

Configure a **slash command** in Slack Bot application and set its Request URL to the Lambda function's API Gateway endpoint.

## Conclusion

This Slack bot is a smart solution that combines real-time Slack interactions with the systematic tracking capabilities of JIRA, all seamlessly operating on the AWS cloud infrastructure. 
The thorough testing and comprehensive documentation ensure its long-term reliability and ease of use.