# Setting Up AWS Builder ID for QAutoRacer

This guide will help you set up your AWS Builder ID to enable the AI features in QAutoRacer.

## What is AWS Builder ID?

AWS Builder ID is a free identity that lets you access certain AWS services without creating a full AWS account. It's designed for developers who want to use AWS services without providing payment information.

## Why Do I Need AWS Builder ID?

QAutoRacer uses Amazon Q Developer for its AI features, including:
- AI-generated track designs
- Adaptive difficulty
- Dynamic commentary
- Visual style generation

To use these features, you need to authenticate with an AWS Builder ID.

## Setting Up Your AWS Builder ID

### Step 1: Create an AWS Builder ID

1. Go to https://profile.aws.amazon.com/
2. Click "Create an AWS Builder ID"
3. Enter your email address
4. Follow the verification steps
5. Create a password

That's it! You now have an AWS Builder ID.

### Step 2: Configure QAutoRacer

1. Launch QAutoRacer
2. From the main menu, select "AWS Builder ID Setup"
3. Enter your AWS Builder ID email address
4. Click "Save Builder ID"

## Using the Free Tier

Amazon Q Developer offers a free tier that includes:
- 2 million tokens per month
- This is more than enough for casual gameplay
- No credit card required
- No AWS account required

## Troubleshooting

If you encounter issues:

1. **Verification Email**: Make sure you've verified your email address
2. **Internet Connection**: Check that your game can connect to the internet
3. **Correct Email**: Ensure you've entered the same email you used for your AWS Builder ID

## Privacy and Security

- Your AWS Builder ID is stored locally on your computer
- It is only used to authenticate with Amazon Q Developer
- No personal data is collected or stored by the game

## Running Without AI Features

If you prefer not to use AWS Builder ID, you can still play QAutoRacer without the AI features:

1. Open config.py
2. Set the following options to False:
   ```python
   "ai_track_generation": False,
   "adaptive_difficulty": False,
   "dynamic_commentary": False,
   "dynamic_music": False,
   ```

This will disable all AI features but allow you to play the game with procedurally generated tracks.