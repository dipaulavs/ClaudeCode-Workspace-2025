# Meta Marketing API Setup Guide

Complete guide to setting up Meta Marketing API for automated campaign creation.

## Prerequisites

- Facebook Business Account
- Facebook Page
- Meta Ads Account
- Meta for Developers App

## Step 1: Create Meta for Developers App

1. Go to https://developers.facebook.com/
2. Click "My Apps" → "Create App"
3. Select "Business" type
4. Fill in app details:
   - App Name: "Automated Ads Manager" (or your choice)
   - Contact Email: your email
5. Click "Create App"

## Step 2: Configure App Permissions

1. In your app dashboard, go to "Add Products"
2. Add "Marketing API"
3. Go to "App Settings" → "Basic"
4. Note your **App ID** and **App Secret**

## Step 3: Generate Access Token

### Option A: Quick Start (Short-lived token)

1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown
3. Click "Generate Access Token"
4. Select these permissions:
   - `ads_management` - Create and manage ads
   - `ads_read` - Read ad data
   - `business_management` - Manage business assets

**Important:** This token expires in 1-2 hours. For production, use Option B.

### Option B: Long-lived Token (Recommended)

1. Get short-lived token from Graph API Explorer (Option A)
2. Exchange for long-lived token:

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}"
```

3. Response contains `access_token` (valid for 60 days)

### Option C: System User Token (Best for automation)

1. Go to Business Settings → System Users
2. Create new system user
3. Assign to ad accounts
4. Generate token with required permissions

**Advantages:**
- Never expires (unless manually revoked)
- Best for server-side automation
- More secure than user tokens

## Step 4: Get Your Ad Account ID

1. Go to https://business.facebook.com/adsmanager/
2. URL format: `https://business.facebook.com/adsmanager/manage/campaigns?act=XXXXXXXXXX`
3. Your Ad Account ID is: `act_XXXXXXXXXX`

**Alternative method:**
```bash
curl -i -X GET \
 "https://graph.facebook.com/v18.0/me/adaccounts?access_token={access-token}"
```

## Step 5: Get Your Page ID

1. Go to your Facebook Page
2. Settings → Page Info
3. Find "Page ID" (numeric value)

**Alternative method:**
```bash
curl -i -X GET \
 "https://graph.facebook.com/v18.0/me/accounts?access_token={access-token}"
```

## Step 6: Configure Credentials

Run the configuration script:

```bash
python3 scripts/configure_meta_ads.py
```

Or manually set environment variables:

```bash
export META_ADS_ACCESS_TOKEN="your_access_token"
export META_ADS_ACCOUNT_ID="act_your_account_id"
export META_PAGE_ID="your_page_id"
export META_ADS_LINK_URL="https://your-website.com"
```

Add to shell profile (~/.zshrc or ~/.bashrc) for persistence.

## Step 7: Install Dependencies

```bash
pip install facebook-business
```

## Step 8: Test Connection

Create test script:

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

access_token = 'your_token'
account_id = 'act_your_account_id'

FacebookAdsApi.init(access_token=access_token)
account = AdAccount(account_id)

# Get account info
print(account.api_get(fields=['name', 'account_id']))

# List campaigns
campaigns = account.get_campaigns(fields=['name', 'id'])
for campaign in campaigns:
    print(f"{campaign['name']}: {campaign['id']}")
```

## Troubleshooting

### Error: "Invalid OAuth access token"

**Cause:** Token expired or invalid

**Solution:**
1. Generate new token from Graph API Explorer
2. Exchange for long-lived token
3. Update META_ADS_ACCESS_TOKEN environment variable

### Error: "Insufficient permissions"

**Cause:** Token missing required permissions

**Solution:**
1. Regenerate token with all required permissions:
   - ads_management
   - ads_read
   - business_management
2. Ensure token is for the correct ad account

### Error: "Ad Account not found"

**Cause:** Incorrect account ID format or unauthorized access

**Solution:**
1. Verify account ID format: `act_XXXXXXXXXX`
2. Ensure your app/user has access to the ad account
3. Check Business Settings → Ad Accounts → Partners

### Rate Limiting

**Cause:** Too many API requests

**Solution:**
- Implement exponential backoff
- Batch requests when possible
- Monitor rate limit headers in API responses

## API Rate Limits

- **Standard tier:** 200 calls per hour per user
- **Development tier:** 200 calls per hour
- **Marketing API:** Higher limits for approved apps

To increase limits:
1. Go to App Dashboard → Marketing API
2. Request Advanced Access
3. Pass App Review for required permissions

## Best Practices

1. **Use System User Tokens** for automation
2. **Store credentials securely** (environment variables, not code)
3. **Implement error handling** for API failures
4. **Log API responses** for debugging
5. **Monitor rate limits** to avoid throttling
6. **Use batch requests** for efficiency
7. **Keep SDK updated** (`pip install --upgrade facebook-business`)

## Security Recommendations

1. **Never commit tokens** to version control
2. **Rotate tokens** periodically
3. **Use minimum required permissions**
4. **Monitor API usage** in Business Settings
5. **Revoke unused tokens** immediately
6. **Use HTTPS only** for API calls

## Resources

- **Meta Marketing API Docs:** https://developers.facebook.com/docs/marketing-apis
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Business Manager:** https://business.facebook.com/
- **SDK Documentation:** https://github.com/facebook/facebook-python-business-sdk
- **Rate Limits:** https://developers.facebook.com/docs/graph-api/overview/rate-limiting/

## Support

- **Meta Developer Community:** https://developers.facebook.com/community/
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/facebook-marketing-api
- **GitHub Issues:** https://github.com/facebook/facebook-python-business-sdk/issues
