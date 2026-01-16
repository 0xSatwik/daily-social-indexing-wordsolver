"""
Facebook Image Poster
Posts images with captions to a Facebook Page
"""

import os
import requests
import json

def post_image_to_facebook(image_path, caption):
    """
    Post an image to a Facebook Page.
    
    Args:
        image_path: Path to the image file
        caption: Post caption/message
    
    Returns:
        Post ID if successful, None otherwise
    """
    access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN', '').strip()
    page_id = os.environ.get('FACEBOOK_PAGE_ID', '964134700097059').strip()  # Default: Wordsolverx
    
    if not access_token:
        print("❌ Facebook Access Token missing. Skipping post.")
        return None
    
    print("Posting image to Facebook...")
    
    try:
        # Upload photo to page
        url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
        
        with open(image_path, 'rb') as f:
            files = {'source': f}
            data = {
                'access_token': access_token,
                'message': caption,
                'published': 'true'
            }
            
            response = requests.post(url, files=files, data=data)
            result = response.json()
        
        if 'id' in result:
            post_id = result['id']
            print(f"✅ Facebook post created! Post ID: {post_id}")
            print(f"🔗 View: https://www.facebook.com/{post_id}")
            return post_id
        else:
            print(f"❌ Facebook post failed: {json.dumps(result, indent=2)}")
            return None
            
    except Exception as e:
        print(f"❌ Error posting to Facebook: {str(e)}")
        return None

if __name__ == "__main__":
    print("Facebook poster module loaded.")
    print("Use post_image_to_facebook() to create posts.")
