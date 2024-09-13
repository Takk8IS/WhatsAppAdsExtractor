# WhatsApp Ads Extractor

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Takk8IS/WhatsAppAdsExtractor)
[![Licence](https://img.shields.io/badge/licence-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub issues](https://img.shields.io/github/issues/Takk8IS/WhatsAppAdsExtractor.svg)](https://github.com/Takk8IS/WhatsAppAdsExtractor/issues)
[![GitHub stars](https://img.shields.io/github/stars/Takk8IS/WhatsAppAdsExtractor.svg)](https://github.com/Takk8IS/WhatsAppAdsExtractor/stargazers)

This Python script asynchronously fetches WhatsApp ads data from Facebook's API, processes it, and exports to CSV. It uses aiohttp for concurrent API requests, extracts relevant ad information including phone numbers and images, and handles multiple ad accounts.

![WhatsApp Ads Extractor](https://github.com/Takk8IS/WhatsAppAdsExtractor/blob/main/images/screenshot-01.png?raw=true)
![WhatsApp Ads Extractor](https://github.com/Takk8IS/WhatsAppAdsExtractor/blob/main/images/screenshot-02.png?raw=true)
![WhatsApp Ads Extractor](https://github.com/Takk8IS/WhatsAppAdsExtractor/blob/main/images/screenshot-03.png?raw=true)

## Features

-   Asynchronous API requests for improved performance
-   Extraction of WhatsApp ad data from multiple Facebook ad accounts
-   Phone number extraction from various ad fields
-   Image URL and filename extraction
-   CSV export of processed ad data
-   Error handling and logging

## API Configuration Manual

This comprehensive guide will walk you through the process of obtaining and configuring the necessary API settings for this application. Follow these detailed instructions to ensure proper setup and functionality.

## Table of Contents

1. [Facebook API Settings](#facebook-api-settings)
2. [Google Sheets API Settings](#google-sheets-api-settings)
3. [Spreadsheet ID](#spreadsheet-id)
4. [Cron Schedule](#cron-schedule)
5. [Other Settings](#other-settings)

## Facebook API Settings

To configure the Facebook API for this application, you'll need to obtain your Facebook App ID, App Secret, and Access Token. Follow these steps:

1. Go to the [Facebook Developers portal](https://developers.facebook.com/).
2. Log in with your Facebook account or create a new one if necessary.
3. Once logged in, click on "My Apps" in the top right corner.
4. Click on "Create App" or select an existing app if you've already created one.
5. If creating a new app, choose the app type that best fits your needs and follow the setup wizard.
6. After creating or selecting your app, navigate to the app dashboard.
7. In the left sidebar, click on "Settings" and then "Basic".
8. Here you'll find your App ID and App Secret. Copy these values and update the corresponding variables in the script:
    ```
    FACEBOOK_APP_ID=your_app_id_here
    FACEBOOK_APP_SECRET=your_app_secret_here
    ```
9. To obtain an Access Token:
   a. In the left sidebar, click on "Tools" and then "Graph API Explorer".
   b. Select your app from the dropdown menu at the top.
   c. Click on "Generate Access Token".
   d. Grant the necessary permissions when prompted.
   e. Copy the generated token and update the variable in the script:
    ```
    FACEBOOK_ACCESS_TOKEN=your_access_token_here
    ```

**Note:** Access Tokens may expire. For long-term use, consider implementing a method to refresh the token automatically.

## Google Sheets API Settings

To use the Google Sheets API, you'll need to set up a project in the Google Cloud Console and create service account credentials. Follow these detailed steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project dropdown at the top of the page and select "New Project".
3. Give your project a name and click "Create".
4. Once the project is created, make sure it's selected in the project dropdown.
5. In the left sidebar, navigate to "APIs & Services" > "Library".
6. Search for "Google Sheets API" and click on it.
7. Click the "Enable" button to enable the API for your project.
8. After enabling, click on "Create Credentials" at the top of the page.
9. For credential type, choose "Service account".
10. Fill in the service account details and click "Create".
11. On the next screen, don't add any roles (unless you need specific permissions).
12. Click "Continue" and then "Done".
13. You'll be taken to the Service Accounts page. Find the account you just created and click on it.
14. In the "Keys" tab, click "Add Key" > "Create new key".
15. Choose JSON as the key type and click "Create".
16. A JSON file will be downloaded to your computer. Keep this file secure as it contains sensitive information.
17. Open the JSON file and locate the `client_email` and `private_key` fields.
18. Update the corresponding variables in the script:
    ```
    GOOGLE_SERVICE_ACCOUNT_EMAIL=your_client_email_here
    GOOGLE_PRIVATE_KEY="your_private_key_here"
    ```
    **Note:** Make sure to keep the quotes around the private key and replace any newline characters with "\n".

## Spreadsheet ID

To find your Google Spreadsheet ID, follow these steps:

1. Open your Google Spreadsheet in a web browser.
2. Look at the URL of the spreadsheet. It will be in this format:
   `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit#gid=0`
3. Copy the [SPREADSHEET_ID] portion of the URL.
4. Update the variable in the script:
    ```
    SPREADSHEET_ID=your_spreadsheet_id_here
    ```

**Important:** Make sure you've shared the spreadsheet with the email address of your Google Service Account (the `client_email` from the JSON file) and given it edit permissions.

## Cron Schedule

The cron schedule determines how often the script will run. The default schedule is daily at midnight UTC (0 0 \* \* \*). If you need a different schedule, modify the CRON_SCHEDULE variable in the script.

Here's a brief explanation of the cron format:

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── day of week (0 - 7) (Sunday = 0 or 7)
│ │ │ └───── month (1 - 12)
│ │ └─────── day of month (1 - 31)
│ └───────── hour (0 - 23)
└─────────── minute (0 - 59)
```

Examples:

-   Run every hour: `0 * * * *`
-   Run every day at 2:30 PM UTC: `30 14 * * *`
-   Run every Monday at 9:00 AM UTC: `0 9 * * 1`

Update the variable in the script with your desired schedule:

```
CRON_SCHEDULE=your_cron_schedule_here
```

## Other Settings

There are two additional settings you may need to adjust:

1. PORT: This sets the port number for your application to listen on. The default is 8015, but you can change it if needed:
    ```
    PORT=your_port_number_here
    ```

## Conclusion

Once you have gathered all the required information and updated the corresponding variables in the script, your API configuration should be complete. Remember to keep your API keys, secrets, and private keys secure and never share them publicly.

For more detailed information on each API and its features, please refer to the official documentation:

-   [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
-   [Google Sheets API Documentation](https://developers.google.com/sheets/api)

If you encounter any issues or need further assistance, consult the troubleshooting guides for each platform or reach out to their respective support channels.

## Requirements

To run this script, you need Python 3.7 or higher. The required packages are listed in the `requirements.txt` file:

```
aiohttp
requests
python-dotenv
```

You can install these dependencies using pip:

```
pip install -r requirements.txt
```

## Configuration

Before running the script, you need to set up your Facebook API credentials. Create a `.env` file in the root directory with the following contents:

```
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
```

Replace `your_app_id`, `your_app_secret`, and `your_access_token` with your actual Facebook API credentials.

## Ad Account IDs

Before running the script, make sure to add your Facebook Ad Account IDs to the `ad_account_ids` list in the script. You can include multiple account IDs if you want to analyze and extract data from several ad accounts:

```python
ad_account_ids = ["act_your_account_id_ads", "act_your_other_account_id_ads"]
```

Replace `"act_your_account_id_ads"` and `"act_your_other_account_id_ads"` with your actual Ad Account IDs. You can add as many account IDs as needed.

## Usage

To run the script, use the following command:

```
python whatsapp_ads_extractor.py
```

The script will fetch WhatsApp ads data from the specified ad accounts, process it, and save the results to a CSV file named `WhatsAppAdsExtractor-YYYY-MM-DD-HH-MM-SS.csv` in the same directory.

## Output

The CSV file will contain the following information for each WhatsApp ad:

-   Date
-   Time
-   Phone Number
-   Source ID
-   Ad ID
-   Thumbnail filename
-   Thumbnail URL
-   Ad Body
-   Conversion type
-   Welcome Text
-   Campaign Name
-   Ad Set Name
-   Ad Name
-   Platform (Facebook, Instagram, or WhatsApp)

## Acknowledgements

-   Facebook Graph API
-   aiohttp library for asynchronous HTTP requests
-   Python's built-in asyncio for asynchronous programming

## Disclaimer

This script is for educational purposes only. Make sure you comply with Facebook's terms of service and have the necessary permissions to access and use the ad data.

## Contributing

We welcome contributions from the community! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Donations

If this project has been helpful, consider making a donation:

**USDT (TRC-20)**: `TGpiWetnYK2VQpxNGPR27D9vfM6Mei5vNA`

Your support helps us continue to develop innovative tools.

## License

This project is licensed under the CC-BY-4.0 License. See the [LICENSE](LICENSE.md) file for more details.

## About Takk™ Innovate Studio

Leading the Digital Revolution as the Pioneering 100% Artificial Intelligence Team.

-   Author: [David C Cavalcante](mailto:davcavalcante@proton.me)
-   LinkedIn: [linkedin.com/in/hellodav](https://www.linkedin.com/in/hellodav/)
-   X: [@Takk8IS](https://twitter.com/takk8is/)
-   Medium: [takk8is.medium.com](https://takk8is.medium.com/)
-   Website: [takk.ag](https://takk.ag/)
