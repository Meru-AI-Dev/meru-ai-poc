# Meru AI POC

Automatically reply to Gmail inbox emails using Google AI (Gemini) or Google Cloud Vertex AI (PaLM 2).

![Group 48095423](https://github.com/Meru-AI-Dev/meru-ai-poc/assets/165311010/4907dac4-1b6f-4774-b669-1764ea9e5a23)
![Group 48095433](https://github.com/Meru-AI-Dev/meru-ai-poc/assets/165311010/5030189a-3a58-45dd-b705-28e23a7a59c8)

- [Meru AI Website](https://meruai.net/)
- [Meru AI Docs](https://docs.meruai.net/)
## Overview

This proof-of-concept (PoC) demonstrates our commitment to delivering cutting-edge technology. The aim of this PoC is to provide investors and enthusiasts with a clear understanding of the potential of Meru AI and encourage them to explore its capabilities firsthand. By showcasing this PoC prior to the $MERU TGE, we aim to engage advisors and venture capitalists more effectively. While we work on the real MVP on the testnet, this serves as a small example to demonstrate the limitless potential of Meru AI.

This proof-of-concept script allows you to:

1. Run the script with a single click.
2. Automatically reply to emails in your Gmail account.
3. Customize the tone of the auto-reply based on Gemini & PaLM 2 prompts.
4. Set rules or filters to reply only to specific emails.
5. Move auto-replied emails to a separate inbox for easy tracking.
6. Ensure your data privacy - the tool runs locally on your PC and does not collect any data. Once you stop the program, it disappears along with any email/data it has read.

## Instructions

### Development Envrionment

To run this proof of concept (PoC), follow these steps:

1. Install Python3 and pip on your machine. If you don't have them installed, you can download Python3 from [here](https://www.python.org/downloads/) and follow the installation guide. For pip installation instructions, refer to the [official documentation](https://pip.pypa.io/en/stable/installation/).

2. Configure the necessary environment variables within the `secrets.env` file, as discussed in the Requirements & Steps to Use sections below.
   
3. Navigate to the project directory in your terminal.

4. Run the following command to install the required packages listed in the `requirements.txt` file:
    ```
    pip3 install -r requirements.txt
    ```

5. Once the installation is complete, run the following command to start the PoC:
    ```
    python3 meru_ai_poc.py
    ```

    The script will automatically respond to emails in your Gmail account based on the configured settings and prompts.

### Tech Stack
- Python3
- Pip3
- Langchain
- Gemini Model (Google AI)
- PaLM 2 Model (Google Cloud Vertex AI)
- IMAP protocol

### Requirements

To use this script, you will need:

1. A Gmail account: If you don't have one, you can create a free account.
2. A Gmail account app password: This is a specific password for the script to access your Gmail account. Follow the provided video tutorial to set it up.
3. A Gemini API secret key: If you already have a Gemini account, sign in. Otherwise, sign up for an account. Follow the instructions at https://ai.google.dev/tutorials/get_started_web to generate a secret key. Keep this key safe, as it allows the tool to access Gemini's text models programmatically.
4. (*Optional*) A Google Cloud Service Account with Vertex AI API: To use PaLM 2, you will need to set up a Google Cloud service account, enable the use of the Vertex AI API (Requires a Billing Account on Google Cloud), and download the `.json` file of the service account key. Set the local path of this key as the value for the `GOOGLE_APPLICATION_CREDENTIALS` variable inside `secrets.env`, for example:
   `GOOGLE_APPLICATION_CREDENTIALS=/Users/skeng/Downloads/palm-2-8819654-e5ekk8f0007zm.json`. Learn more about creating a Google Cloud service account key [here](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console) in the official Google documentation.

#### Gemini VS. PaLM 2

The latest update to this PoC now supports switching between using the Google AI (Gemini) language model and the Google Cloud Vertex AI (PaLM 2) language model.

- Utilizing Gemini is free of charge.
- Utilizing PaLM 2 entails costs and necessitates setting up billing on your Google Cloud account, as Google is deprecating the PaLM 2 API while maintaining access to this API through Vertex AI. Reference: [Google's PaLM Deprecation Notice](https://ai.google.dev/palm_docs/deprecation).

For PaLM 2, it is distinct from the Google PaLM integration. Google has opted to provide an enterprise version of PaLM through GCP, supporting the models made accessible there. By default, Google Cloud does not employ customer data to train its foundation models as part of Google Cloud's AI/ML Privacy Commitment. Additional information on how Google processes data can be found in [Google's Customer Data Processing Addendum (CDPA)](https://cloud.google.com/terms/data-processing-addendum).

The PoC facilitates switching between Gemini and PaLM 2 based on the configured environment variables within the `secrets.env` file. If you add the `GOOGLE_APPLICATION_CREDENTIALS`, which is required for utilizing PaLM 2, Meru AI will use PaLM 2, even if the `GOOGLE_API_KEY` is configured, which is necessary for Gemini. To use Gemini, keep the `GOOGLE_APPLICATION_CREDENTIALS` empty and only configure the `GOOGLE_API_KEY` value.

### Steps to Use

1. Download and extract the provided folder.
2. Log into your Gmail account and create a new label/folder called "meru-ai-replies". This is important to prevent the tool from responding to the same email repeatedly.
3. Configure your settings and prompts by following the provided template formats.
4. Configure "secrets.env" file:

    - Open the file with a text editor.
    - Fill in the values for `GOOGLE_API_KEY`, `email_address`, and `gmail_app_password` as detailed in the requirements section. Configuring `GOOGLE_APPLICATION_CREDENTIALS` is optional for utilizing the PaLM 2 enterprise edition.
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
