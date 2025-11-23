# API Integration Guide

## Frontend-Backend Integration

The spell checker now features a robust frontend-backend integration with automatic fallback capabilities.

## Architecture

### Backend API (Flask)
- **Endpoint**: `/api/check`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **CORS**: Enabled for GitHub Pages and local development

### Frontend (Vanilla JavaScript)
- **Primary Mode**: Calls backend API for spell checking
- **Fallback Mode**: Uses client-side algorithm if backend is unavailable
- **Smart Retry**: Tries multiple endpoints with timeout protection

## API Endpoints

### POST /api/check
Check and correct spelling in the provided text.

**Request:**
```json
{
  "text": "This is sampl text with erors"
}
```

**Response (Success):**
```json
{
  "success": true,
  "original": "This is sampl text with erors",
  "corrected": "This is sample text with errors",
  "has_corrections": true
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message here"
}
```

### GET /api/health
Health check endpoint to verify API availability.

**Response:**
```json
{
  "status": "healthy",
  "service": "spell-checker-api"
}
```

## Frontend Configuration

The frontend is configured to try multiple API endpoints in sequence:

```javascript
const API_CONFIG = {
    endpoints: [
        'https://spell-checker-production.up.railway.app/api/check', // Production
        'http://localhost:5000/api/check',  // Local dev
        'http://127.0.0.1:5000/api/check'   // Alternative local
    ],
    timeout: 5000 // 5 seconds per endpoint
};
```

## How It Works

1. **User Input**: User enters text and clicks "Check Spelling"
2. **Backend Attempt**: Frontend tries each configured endpoint in order
3. **Success**: If any endpoint responds successfully, use backend corrections
4. **Fallback**: If all endpoints fail, use client-side spell checker
5. **User Notification**: Display appropriate success/offline message

## Deployment Options

### Option 1: GitHub Pages Only (Client-Side)
- No backend setup required
- Uses client-side spell checker with limited dictionary
- Works immediately after enabling GitHub Pages
- Good for: Quick demos, lightweight applications

### Option 2: Full Stack (Backend + Frontend)
- Deploy backend to Heroku, Railway, or other hosting
- Update `API_CONFIG.endpoints` in `docs/app.js` with your backend URL
- Best spell checking accuracy using trained model
- Good for: Production applications, high accuracy requirements

### Option 3: Hybrid (Automatic Fallback)
- Current default configuration
- Tries backend first, falls back to client-side
- Best of both worlds: Accuracy when available, always functional
- Good for: All use cases

## Local Development

### 1. Start Backend Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
python main.py
# Server starts at http://localhost:5000
```

### 2. Test API
```bash
# Health check
curl http://localhost:5000/api/health

# Spell check
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "This is sampl text"}'
```

### 3. Test Frontend
```bash
# Open frontend in browser
open docs/index.html
# Or use a local server:
cd docs && python -m http.server 8000
open http://localhost:8000
```

## CORS Configuration

The backend is configured to accept requests from:
- `https://vaporjawn.github.io` (GitHub Pages)
- `http://localhost:*` (Local development)
- `http://127.0.0.1:*` (Alternative local)

To add additional origins:

```python
# In main.py
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://vaporjawn.github.io",
            "https://your-custom-domain.com",
            "http://localhost:*"
        ]
    }
})
```

## Production Deployment

### Backend Deployment (Railway/Heroku)

1. **Ensure requirements.txt includes Flask-CORS:**
   ```
   Flask==3.1.0
   Flask-CORS==5.0.0
   gunicorn==23.0.0
   ```

2. **Deploy to your platform:**
   - Railway: Connect GitHub repo, auto-deploys
   - Heroku: `git push heroku master`

3. **Get your deployment URL:**
   - Railway: `https://your-app.up.railway.app`
   - Heroku: `https://your-app.herokuapp.com`

### Frontend Update

Update `docs/app.js` with your backend URL:

```javascript
const API_CONFIG = {
    endpoints: [
        'https://your-actual-backend-url.com/api/check',
        'http://localhost:5000/api/check'
    ],
    timeout: 5000
};
```

Commit and push to deploy via GitHub Actions.

## Testing Integration

### Test Backend API
```bash
# From command line
curl -X POST https://your-backend-url.com/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "tset text with erors"}'
```

### Test Frontend
1. Open browser developer console
2. Go to your GitHub Pages URL
3. Enter text and click "Check Spelling"
4. Check console logs for connection status:
   - `✓ Connected to backend API: [url]` - Success
   - `✗ Failed to connect to [url]` - Trying fallback
   - `Using client-side spell checker as fallback` - Offline mode

## Security Features

- **CORS Protection**: Only allowed origins can access API
- **Input Validation**: Text length limits and sanitization
- **Rate Limiting**: Consider adding rate limiting for production
- **HTTPS**: Use HTTPS for all production deployments
- **Security Headers**: Implemented in Flask backend

## Troubleshooting

### Backend not responding
- Check if backend server is running
- Verify URL in API_CONFIG matches your deployment
- Check CORS configuration includes your frontend domain
- Review backend logs for errors

### CORS errors
- Verify frontend domain is in CORS origins list
- Ensure credentials are not being sent (CORS simple requests)
- Check browser console for specific CORS error messages

### Client-side fallback always used
- Check browser console for connection error messages
- Verify backend API is accessible (try curl command)
- Check network tab in browser dev tools
- Ensure API returns correct JSON format

## Future Enhancements

Potential improvements for the integration:
- [ ] Add WebSocket support for real-time checking
- [ ] Implement caching to reduce API calls
- [ ] Add batch processing for large documents
- [ ] Include confidence scores in corrections
- [ ] Add language detection and multi-language support
- [ ] Implement user authentication for premium features
- [ ] Add rate limiting and usage analytics

## Performance Optimization

Current optimizations:
- 5-second timeout per endpoint
- Multiple endpoint fallback
- Client-side caching in dictionary
- Minimal payload size
- Asynchronous API calls

## Support

For issues with integration:
1. Check browser console for error messages
2. Verify backend is deployed and accessible
3. Review CORS configuration
4. Test with curl to isolate frontend/backend issues
5. Open an issue on GitHub with error details

---

**Last Updated**: November 23, 2025
**Author**: Victor Williams
**Repository**: https://github.com/Vaporjawn/Spell-Checker
