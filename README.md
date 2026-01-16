# Daily Social Indexing & Pinterest/Facebook Image Pin Automation

Automated system that:
1. **Submits URLs to Google Indexing API** (25 dynamic URLs + pages.txt)
2. **Creates Pinterest Image Pins** (5 puzzle types at staggered times)
3. **Posts to Facebook** (same images as Pinterest)

## Schedule (IST)

| Time | Action |
|------|--------|
| 12:00 AM | Submit all URLs for indexing + Wordle Pin |
| 12:30 AM | Quordle Pin |
| 1:00 AM | Colordle Pin |
| 2:00 AM | Semantle Pin |
| 3:00 AM | Phoodle Pin |

## URL Format
```
https://wordsolverx.com/{puzzle}-answer-for-{month}-{day}-{year}
```

## Indexing Coverage
- **Today** (e.g., January 17)
- **Tomorrow +1** (January 18)
- **Tomorrow +2** (January 19)
- **Yesterday -1** (January 16)
- **Yesterday -2** (January 15)
- **Plus** any URLs in `pages.txt`

## Pinterest Board IDs (Hardcoded)
- Wordle: `924434329702687588`
- Quordle: `924434329702687592`
- Colordle: `924434329702687590`
- Semantle: `924434329702687594`
- Phoodle: `924434329702687593`

## GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Base64-encoded service account JSON for Indexing API |
| `PINTEREST_ACCESS_TOKEN` | Pinterest Sandbox access token |
| `PINTEREST_USE_SANDBOX` | Set to `true` for Sandbox, `false` for Production |
| `FACEBOOK_ACCESS_TOKEN` | Facebook Page access token |
| `FACEBOOK_PAGE_ID` | Facebook Page ID (default: Wordsolverx) |

## Local Testing

1. Create `.env` file:
```
PINTEREST_ACCESS_TOKEN=pina_...
PINTEREST_USE_SANDBOX=true
FACEBOOK_ACCESS_TOKEN=your_token
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Test image generation:
```bash
python image_generator.py
```

4. Test indexing:
```bash
ACTION=indexing python main.py
```

5. Test social post:
```bash
ACTION=social PUZZLE_TYPE=wordle python main.py
```

## Adding Custom URLs

Edit `pages.txt` to add URLs for indexing (one per line).

## Switching Pinterest to Production

1. Request "Standard Access" at [Pinterest Developer Portal](https://developers.pinterest.com/apps/)
2. Once approved, regenerate tokens with `pinterest_oauth.py` (type `no` for Production)
3. Update `PINTEREST_ACCESS_TOKEN` secret
4. Set `PINTEREST_USE_SANDBOX=false` in GitHub Secrets
