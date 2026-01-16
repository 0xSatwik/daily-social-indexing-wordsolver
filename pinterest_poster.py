"""
Pinterest Image Pin Poster
Uploads images as pins to Pinterest using the API v5
"""

import os
import requests
import json

def upload_image_to_pinterest(image_path, title, description, link, board_id):
    """
    Upload an image as a pin to Pinterest.
    
    Args:
        image_path: Path to the image file
        title: Pin title
        description: Pin description
        link: URL the pin links to
        board_id: Target Pinterest board ID
    
    Returns:
        Pin ID if successful, None otherwise
    """
    access_token = os.environ.get('PINTEREST_ACCESS_TOKEN', '').strip()
    use_sandbox = os.environ.get('PINTEREST_USE_SANDBOX', 'true').lower() == 'true'
    
    if not access_token:
        print("❌ Pinterest Access Token missing. Skipping upload.")
        return None
    
    if not board_id:
        print("❌ Pinterest Board ID missing. Skipping upload.")
        return None
    
    base_url = "https://api-sandbox.pinterest.com" if use_sandbox else "https://api.pinterest.com"
    
    print(f"Uploading image pin to Pinterest ({'Sandbox' if use_sandbox else 'Production'})...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        # For image pins, we upload directly with base64 encoding
        import base64
        
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Determine media type from file extension
        ext = os.path.splitext(image_path)[1].lower()
        media_type = "image/png" if ext == ".png" else "image/jpeg"
        
        pin_url = f"{base_url}/v5/pins"
        
        pin_payload = {
            "board_id": board_id,
            "media_source": {
                "source_type": "image_base64",
                "content_type": media_type,
                "data": image_data
            },
            "title": title[:100],  # Pinterest title limit
            "description": description[:500],  # Pinterest description limit
            "link": link
        }
        
        headers["Content-Type"] = "application/json"
        
        response = requests.post(pin_url, headers=headers, json=pin_payload)
        result = response.json()
        
        if 'id' in result:
            pin_id = result['id']
            print(f"✅ Pinterest Pin created! Pin ID: {pin_id}")
            print(f"🔗 View: https://www.pinterest.com/pin/{pin_id}/")
            return pin_id
        else:
            print(f"❌ Pinterest Pin creation failed: {json.dumps(result, indent=2)}")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading to Pinterest: {str(e)}")
        return None

if __name__ == "__main__":
    # Test upload (requires valid credentials)
    print("Pinterest poster module loaded.")
    print("Use upload_image_to_pinterest() to upload pins.")
