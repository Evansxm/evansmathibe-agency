# Google Indexing API Setup Instructions

To enable automated indexing for Evans Mathibe Agency, follow these steps:

1. Enable the Indexing API:
   - Go to the Google Cloud Console.
   - Create a new project or select an existing one.
   - Navigate to "APIs & Services" > "Library".
   - Search for "Indexing API" and click "Enable".

2. Create a Service Account:
   - Go to "APIs & Services" > "Credentials".
   - Click "Create Credentials" > "Service Account".
   - Give it a name (e.g., "seo-automation") and click "Create and Continue".
   - Skip optional roles and click "Done".

3. Generate and Download JSON Key:
   - In the Service Accounts list, click on the newly created account.
   - Go to the "Keys" tab.
   - Click "Add Key" > "Create New Key".
   - Select "JSON" and click "Create".
   - Securely save the downloaded JSON file; you will need its contents for the GitHub Secret.

4. Authorize in Google Search Console:
   - Copy the email address of the service account (e.g., seo-automation@project-id.iam.gserviceaccount.com).
   - Go to Google Search Console and select your property (https://evansxm.github.io/evansmathibe-agency/).
   - Navigate to "Settings" > "Users and permissions".
   - Click "Add User".
   - Paste the service account email and set the Permission to "Owner".
   - This authorization is mandatory for the Indexing API to accept requests.
