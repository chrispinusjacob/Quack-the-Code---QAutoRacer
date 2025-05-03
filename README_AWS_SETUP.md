# Setting Up AWS Builder ID for QAutoRacer

This guide will help you set up your AWS Builder ID to enable the AI features in QAutoRacer.

## What is AWS Builder ID?

AWS Builder ID is a free account that allows you to access AWS services. It's separate from an AWS account and is designed for developers who want to use AWS services without creating a full AWS account.

## Why Do I Need AWS Builder ID?

QAutoRacer uses Amazon Q Developer for its AI features, including:
- AI-generated track designs
- Adaptive difficulty
- Dynamic commentary
- Visual style generation

To use these features, you need to authenticate with AWS.

## Setting Up Your AWS Builder ID

### Step 1: Create an AWS Builder ID

1. Go to https://profile.aws.amazon.com/
2. Click "Create an AWS Builder ID"
3. Follow the instructions to create your account

### Step 2: Create Access Keys

1. Sign in to the AWS Management Console using your Builder ID
2. Go to the IAM service
3. Click on "Users" in the left navigation pane
4. Click "Add user"
5. Enter a username (e.g., "QAutoRacer")
6. Select "Programmatic access"
7. Click "Next: Permissions"
8. Click "Attach existing policies directly"
9. Search for and select "AmazonQFullAccess"
10. Click "Next: Tags" (you can skip this step)
11. Click "Next: Review"
12. Click "Create user"
13. **Important**: Copy your Access Key ID and Secret Access Key. You will need these for the game.

### Step 3: Configure QAutoRacer

1. Launch QAutoRacer
2. From the main menu, select "AWS Setup"
3. Enter your AWS Builder ID
4. Enter your Access Key ID and Secret Access Key
5. Select your AWS Region (usually "us-east-1")
6. Click "Test Connection" to verify your credentials
7. Click "Save Credentials" to save your settings

## Using the Free Tier

AWS offers a Free Tier that includes:
- Amazon Q Developer: 2 million tokens per month
- This is more than enough for casual gameplay

## Troubleshooting

If you encounter issues:

1. **Connection Failed**: Verify your Access Key ID and Secret Access Key
2. **Permission Denied**: Make sure you attached the "AmazonQFullAccess" policy
3. **Region Issues**: Try changing to a different region, such as "us-east-1"

## Privacy and Security

- Your AWS credentials are stored locally on your computer
- They are only used to authenticate with AWS services
- No personal data is collected or stored by the game

## Running Without AWS

If you prefer not to use AWS, you can still play QAutoRacer without the AI features:

1. Open config.py
2. Set the following options to False:
   ```python
   "ai_track_generation": False,
   "adaptive_difficulty": False,
   "dynamic_commentary": False,
   "dynamic_music": False,
   ```

This will disable all AI features but allow you to play the game with procedurally generated tracks.