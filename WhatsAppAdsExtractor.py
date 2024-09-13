# Advanced Python Script for Asynchronous WhatsApp Ads Data Extraction and Processing
#
# This enterprise-grade application leverages asynchronous programming to efficiently fetch,
# process, and export WhatsApp ads data from Facebook's Graph API. Key features include:
#
# - Utilization of aiohttp for high-performance concurrent API requests
# - Robust error handling and logging for production environments
# - Scalable architecture supporting multiple ad accounts
# - Sophisticated data extraction algorithms for phone numbers and image metadata
# - Efficient data processing and formatting for business intelligence purposes
# - Automated CSV export for seamless integration with data analysis workflows
#
# The core algorithm encompasses access token validation, parallel data fetching,
# WhatsApp ad filtering, comprehensive data extraction and normalization, concluding
# with a thread-safe CSV export process.
#
# This project is licensed under the CC-BY-4.0 License.
#
# Developed by: David C Cavalcante
# Role: Lead Software Engineer, Takk™ Innovate Studio
# Professional Network: linkedin.com/in/hellodav
# Technical Blog: takk8is.medium.com
# Corporate Website: takk.ag

import requests
import csv
from datetime import datetime
import json
import re
from typing import List, Dict, Any
from aiohttp import ClientSession
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

FACEBOOK_API_VERSION = "v20.0"
FACEBOOK_API_BASE_URL = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}"

FACEBOOK_APP_ID = "your_app_id"
FACEBOOK_APP_SECRET = "your_app_secret"
FACEBOOK_ACCESS_TOKEN = "your_access_token"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdPlatform(Enum):
    FACEBOOK = "Fb_Ads"
    INSTAGRAM = "IG_Ads"
    WHATSAPP = "WA_Ads"

@dataclass
class AdData:
    Data: str
    Hora: str
    Número: str
    SourceID: str
    AdID: str
    Thumbnail: str
    ThumbnailURL: str
    Body: str
    Conversion: str
    Text: str
    Campanha: str
    Conjunto: str
    Anúncio: str
    Platform: str

class FacebookAPIError(Exception):
    """Custom exception for Facebook API errors"""
    pass

async def validate_access_token() -> bool:
    async with ClientSession() as session:
        try:
            async with session.get(
                f"{FACEBOOK_API_BASE_URL}/debug_token",
                params={
                    "input_token": FACEBOOK_ACCESS_TOKEN,
                    "access_token": f"{FACEBOOK_APP_ID}|{FACEBOOK_APP_SECRET}",
                },
            ) as response:
                if response.status != 200:
                    error_data = await response.json()
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                    raise FacebookAPIError(f"Error validating access token: {error_message}")

                data = await response.json()
                logger.info("Access token validation: %s", data)
                return data["data"]["is_valid"]
        except FacebookAPIError as error:
            logger.error(str(error))
            return False
        except Exception as error:
            logger.error("Unexpected error validating access token: %s", error)
            return False

def extract_phone_number(ad_data: Dict[str, Any]) -> str:
    from_number_id = ad_data.get("creative", {}).get("object_story_spec", {}).get("link_data", {}).get("call_to_action", {}).get("value", {}).get("fromNumberId")
    if from_number_id:
        return from_number_id

    link = ad_data.get("creative", {}).get("object_story_spec", {}).get("link_data", {}).get("link", "")
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:wa\.me\/|api\.whatsapp\.com\/send\?phone=)(\d+)"
    match = re.search(pattern, link)
    if match:
        return match.group(1)

    message = ad_data.get("creative", {}).get("object_story_spec", {}).get("link_data", {}).get("message", "")
    phone_pattern = r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\s?)?\d{4}[-.\s]?\d{4}\b"
    phone_match = re.search(phone_pattern, message)
    if phone_match:
        return phone_match.group().replace(" ", "").replace("-", "").replace(".", "")

    return "N/A"

async def get_whatsapp_ads_data() -> List[AdData]:
    ad_account_ids = ["act_your_account_id_ads", "act_your_other_account_id_ads"]
    all_whatsapp_ads_data = []

    async with ClientSession() as session:
        tasks = [fetch_account_data(session, account_id) for account_id in ad_account_ids]
        results = await asyncio.gather(*tasks)

    for account_data in results:
        all_whatsapp_ads_data.extend(account_data)

    return all_whatsapp_ads_data

async def fetch_account_data(session: ClientSession, account_id: str) -> List[AdData]:
    try:
        async with session.get(
            f"{FACEBOOK_API_BASE_URL}/{account_id}/ads",
            params={
                "access_token": FACEBOOK_ACCESS_TOKEN,
                "fields": "id,name,created_time,creative{id,object_story_spec{link_data{call_to_action{type,value},message,page_welcome_message,link}},image_url},adset{id,name,campaign{id,name}},insights{clicks,impressions,reach,spend}",
                "limit": 1000,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()

            whatsapp_ads = [
                ad for ad in data["data"]
                if ad.get("creative", {}).get("object_story_spec", {}).get("link_data", {}).get("call_to_action", {}).get("type") == "WHATSAPP_MESSAGE"
            ]

            return [format_ad_data(ad) for ad in whatsapp_ads]
    except Exception as error:
        logger.error("Error fetching data for account %s: %s", account_id, error)
        return []

def extract_image_name(image_url: str) -> str:
    """Extract the file name from the image URL, ignoring any query parameters."""
    if image_url:
        image_path = image_url.split('?', 1)[0]
        return image_path.rsplit('/', 1)[-1]
    return "N/A"

def determine_ad_platform(ad: Dict[str, Any]) -> AdPlatform:
    if "whatsapp" in ad.get("name", "").lower() or "wa" in ad.get("name", "").lower():
        return AdPlatform.WHATSAPP
    elif "instagram" in ad.get("name", "").lower() or "ig" in ad.get("name", "").lower():
        return AdPlatform.INSTAGRAM
    return AdPlatform.FACEBOOK

def format_ad_data(ad: Dict[str, Any]) -> AdData:
    created_date = datetime.strptime(ad["created_time"], "%Y-%m-%dT%H:%M:%S%z")
    link_data = ad.get("creative", {}).get("object_story_spec", {}).get("link_data", {})
    page_welcome_message = link_data.get("page_welcome_message", "{}")
    welcome_text = "N/A"

    try:
        parsed_message = json.loads(page_welcome_message)
        welcome_text = parsed_message.get("text_format", {}).get("message", {}).get("text", "N/A")
    except json.JSONDecodeError:
        logger.error("Error parsing page_welcome_message for ad %s", ad['id'])

    phone_number = extract_phone_number(ad)
    image_url = ad.get("creative", {}).get("image_url", "N/A")
    image_name = extract_image_name(image_url)
    platform = determine_ad_platform(ad)

    return AdData(
        Data=created_date.strftime("%d/%m/%Y"),
        Hora=created_date.strftime("%H:%M:%S"),
        Número=phone_number,
        SourceID=ad.get("adset", {}).get("campaign", {}).get("id", "N/A"),
        AdID=ad.get("adset", {}).get("id", "N/A"),
        Thumbnail=image_name,
        ThumbnailURL=image_url,
        Body=link_data.get("message", "N/A").replace("[", "").replace("]", "").strip(),
        Conversion=platform.value,
        Text=welcome_text,
        Campanha=ad.get("adset", {}).get("campaign", {}).get("name", "N/A"),
        Conjunto=ad.get("adset", {}).get("name", "N/A"),
        Anúncio=ad.get("name", "N/A"),
        Platform=platform.name
    )

async def main():
    try:
        if not await validate_access_token():
            logger.error("Facebook access token is invalid or expired. Please update the token and try again.")
            return

        whatsapp_ads_data = await get_whatsapp_ads_data()

        if not whatsapp_ads_data:
            logger.warning("No WhatsApp ads data retrieved. Check your account settings and try again.")
            return

        logger.info("WhatsApp Ads Data:")
        logger.info(json.dumps([ad.__dict__ for ad in whatsapp_ads_data], indent=2))

        filename = f"WhatsAppAdsExtractor-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = AdData.__annotations__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            ads_written = 0
            for ad in whatsapp_ads_data:
                if ad.Body != "N/A":
                    writer.writerow(ad.__dict__)
                    ads_written += 1

        logger.info("CSV file saved as %s with %d ads", filename, ads_written)
    except Exception as error:
        logger.error("Error in main function: %s", error)

if __name__ == "__main__":
    asyncio.run(main())
