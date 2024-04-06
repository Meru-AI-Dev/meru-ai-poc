# Meru AI POC

Automatically reply to Gmail inbox emails using Google AI (Gemini).

![Group 48095423](https://github.com/Meru-AI-Dev/meru-ai-poc/assets/165311010/4907dac4-1b6f-4774-b669-1764ea9e5a23)

- [Meru AI Website](https://meruai.net/)
- [Meru AI Docs](https://docs.meruai.net/)
## Overview

This proof-of-concept (PoC) demonstrates our commitment to delivering cutting-edge technology. The aim of this PoC is to provide investors and enthusiasts with a clear understanding of the potential of Meru AI and encourage them to explore its capabilities firsthand. By showcasing this PoC prior to the $MERU TGE, we aim to engage advisors and venture capitalists more effectively. While we work on the real MVP on the testnet, this serves as a small example to demonstrate the limitless potential of Meru AI.

This proof-of-concept script allows you to:

1. Run the script with a single click.
2. Automatically reply to emails in your Gmail account.
3. Customize the tone of the auto-reply based on Gemini prompts.
4. Set rules or filters to reply only to specific emails.
5. Move auto-replied emails to a separate inbox for easy tracking.
6. Ensure your data privacy - the tool runs locally on your PC and does not collect any data. Once you stop the program, it disappears along with any email/data it has read.

## Instructions

### Development Envrionment

To run this proof of concept (PoC), follow these steps:

1. Install Python3 and pip on your machine. If you don't have them installed, you can download Python3 from [here](https://www.python.org/downloads/) and follow the installation guide. For pip installation instructions, refer to the [official documentation](https://pip.pypa.io/en/stable/installation/).

2. Navigate to the project directory in your terminal.

3. Run the following command to install the required packages listed in the `requirements.txt` file:
    ```
    pip3 install -r requirements.txt
    ```

4. Once the installation is complete, run the following command to start the PoC:
    ```
    python3 meru_ai_poc.py
    ```

    The script will automatically respond to emails in your Gmail account based on the configured settings and prompts.

### Tech Stack
- Python3
- Pip3
- Langchain
- Gemini AI Model
- IMAP protocol

### Requirements

To use this script, you will need:

1. A Gmail account: If you don't have one, you can create a free account.
2. A Gmail account app password: This is a specific password for the script to access your Gmail account. Follow the provided video tutorial to set it up.
3. A Gemini API secret key: If you already have a Gemini account, sign in. Otherwise, sign up for an account. Follow the instructions at https://ai.google.dev/tutorials/get_started_web to generate a secret key. Keep this key safe, as it allows the tool to access Gemini's text models programmatically.

### Steps to Use

1. Download and extract the provided folder.
2. Log into your Gmail account and create a new label/folder called "meru-ai-replies". This is important to prevent the tool from responding to the same email repeatedly.
3. Configure your settings and prompts by following the provided template formats.
4. Configure "secrets.env" file:

    - Open the file with a text editor.
    - Fill in the values for `GOOGLE_API_KEY`, `email_address`, and `gmail_app_password` as explained in the requirements section.
    - Set `attempt_interval_in_seconds` to determine how often the tool checks your inbox. The default is 300 seconds (5 minutes), but you can adjust it as needed. Keep in mind that a lower interval may increase the tool's resource usage.
    - Set `days_interval` to determine how far back the tool reads your emails. The default is 0, meaning it only checks emails received today. Increase the value to check emails from previous days.

5. Configure "genai_options.csv" file:

    - In the `filter_type` column, enter values 1, 2, or 3 to define the email rules the script will check:
      - 1: Filter by email address only.
      - 2: Filter by subject only.
      - 3: Filter by both email address and subject.
    - In the `filters` column, enter the email address or subject header. If `filter_type` is set to 3, separate multiple values with a semicolon (;).
    - In the `genai_prompt` column, write your prompt for each filter.

6. Run the `meru_ai_poc` application and witness the magic!

### Need help
If you encounter any issues or need assistance, please create an issue in this repository [here](https://github.com/Meru-AI-Dev/meru-ai-poc/issues). Our development team will promptly respond to help you resolve it.
