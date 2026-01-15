# Google Sheets Configuration Guide

To use the Google Spreadsheet export function, you need to configure a "Service Account" on Google Cloud. It's free and takes about 5 minutes.

## Quick Summary
Your program needs a "bot" (Service Account) to represent it in order to modify spreadsheets.

## Detailed Steps

### 1. Create a Project on Google Cloud
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the dropdown menu in the top left (next to the Google Cloud logo) and select **"New Project"**.
3. Give it a name (e.g., `Text-Analyzer`) and click **"Create"**.
4. Select the project you just created.

### 2. Enable Required APIs
1. In the menu on the left, go to **"APIs & Services" > "Library"**.
2. Search for **"Google Sheets API"**, click on it, and press **"Enable"**.
3. Return to the Library, search for **"Google Drive API"**, click on it, and press **"Enable"**.

### 3. Create the Service Account (The "Bot")
1. Go to **"APIs & Services" > "Credentials"**.
2. Click on **"+ CREATE CREDENTIALS"** (at the top) and choose **"Service account"**.
3. Give it a name (e.g., `analyzer-bot`) and click **"Create and Continue"**.
4. (Optional) Under "Select a role", choose **"Editor"** (Basic > Editor). Click **"Continue"** and then **"Done"**.

### 4. Download the JSON Key
1. In the "Service Accounts" list, click on the email address of the bot you just created (e.g., `analyzer-bot@...`).
2. Go to the **"KEYS"** tab (at the top).
3. Click **"ADD KEY" > "Create new key"**.
4. Choose **JSON** and click **"Create"**.
5. A file will be downloaded to your computer.

### 5. Final Configuration
1. **Rename** the downloaded file to `credentials.json`.
2. **Move it** to the main folder of this project (`Text-Analyzer-CLI/`).
3. **Important:** Open the `credentials.json` file and copy the `"client_email"` address.
4. Go to your browser, create a new Google Sheet (or use an existing one).
5. Click **"Share"** and paste the bot's email (`client_email`), giving it **Editor** permissions.
6. Copy the **Name** of the sheet (e.g., "Text Analyzer Analysis").

You are now ready! When the program asks for the sheet name, use the one you chose.
