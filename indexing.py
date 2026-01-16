"""
Google Indexing API Integration
Submits URLs for indexing using Google's Indexing API
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_service():
    """Get authenticated Google Indexing API service"""
    # Try to load from environment variable (base64 encoded JSON)
    service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', '')
    
    if service_account_json:
        try:
            import base64
            json_str = base64.b64decode(service_account_json).decode('utf-8')
            credentials_info = json.loads(json_str)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info, scopes=SCOPES
            )
            return build('indexing', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error loading service account from env: {e}")
    
    # Try to load from file
    sa_file = os.path.join(os.path.dirname(__file__), 'service_account.json')
    if os.path.exists(sa_file):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                sa_file, scopes=SCOPES
            )
            return build('indexing', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error loading service account from file: {e}")
    
    print("⚠️ No Google Service Account credentials found. Skipping indexing.")
    return None

def submit_url_for_indexing(service, url, action="URL_UPDATED"):
    """
    Submit a single URL for indexing.
    
    Args:
        service: Google API service
        url: URL to submit
        action: "URL_UPDATED" or "URL_DELETED"
    
    Returns:
        True if successful, False otherwise
    """
    try:
        body = {
            "url": url,
            "type": action
        }
        response = service.urlNotifications().publish(body=body).execute()
        print(f"✅ Submitted: {url}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print(f"❌ Permission denied for {url} - Check Search Console ownership")
        elif "429" in error_msg:
            print(f"⚠️ Rate limited for {url} - Try again later")
        else:
            print(f"❌ Error submitting {url}: {error_msg}")
        return False

def submit_urls_for_indexing(urls, action="URL_UPDATED"):
    """
    Submit multiple URLs for indexing.
    
    Args:
        urls: List of URLs to submit
        action: "URL_UPDATED" or "URL_DELETED"
    """
    service = get_service()
    
    if not service:
        print("Cannot submit URLs - no valid credentials")
        return
    
    success_count = 0
    fail_count = 0
    
    print(f"\n📤 Submitting {len(urls)} URLs for indexing...")
    print("-" * 50)
    
    for url in urls:
        if submit_url_for_indexing(service, url, action):
            success_count += 1
        else:
            fail_count += 1
    
    print("-" * 50)
    print(f"📊 Results: {success_count} succeeded, {fail_count} failed")

if __name__ == "__main__":
    # Test with a single URL
    test_urls = [
        "https://wordsolverx.com/wordle-answer-for-january-17-2026"
    ]
    submit_urls_for_indexing(test_urls)
