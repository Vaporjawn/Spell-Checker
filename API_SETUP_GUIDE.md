# API and Frontend Integration Setup Guide

## Overview

Your Spell Checker now has a fully functional REST API with CORS support and an integrated frontend. This guide covers everything you need to know to use the API.

## ✅ What's Already Implemented

### Backend API ([main.py](main.py))
- ✅ **CORS Configuration**: Enabled for GitHub Pages and localhost
- ✅ **API Endpoints**:
  - `POST /api/check` - Spell checking
  - `GET /api/health` - Health check
  - `GET /api/status` - Component status
  - `GET /api/metrics` - Metrics endpoint
- ✅ **Security Features**:
  - Security headers (X-Frame-Options, CSP, etc.)
  - Input validation (10,000 character limit)
  - Error handling
  - Secure session configuration
- ✅ **Dependencies**: Flask 3.1.0, Flask-CORS 5.0.0

### Frontend Integration ([docs/app.js](docs/app.js))
- ✅ **API Client**: Auto-connects to backend API
- ✅ **Fallback System**: Client-side spell checker if API unavailable
- ✅ **Error Handling**: User-friendly notifications
- ✅ **Multiple Endpoints**: Tries production, then local dev
- ✅ **Enhanced UX**: Loading states, notifications, retry logic

## 🚀 Quick Start

### 1. Start the API Server

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the server
python main.py
```

The API will start on `http://127.0.0.1:5000`

**Note for macOS users**: If port 5000 is in use by AirPlay Receiver, you can either:
- Disable AirPlay Receiver: System Settings → General → AirDrop & Handoff → AirPlay Receiver
- Use a different port:
  ```bash
  # In main.py, change the last line to:
  app.run(port=5001)
  ```

### 2. Test the API

Using curl:
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Spell check
curl -X POST http://127.0.0.1:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
```

Using the Python test client:
```bash
python test_api_client.py
```

### 3. Use the Frontend

1. **Start the Flask server** (see step 1)
2. **Open the frontend**: Open [docs/index.html](docs/index.html) in your browser
3. **Start typing**: The frontend will automatically connect to the API
4. **Check spelling**: Click "Check Spelling" or press Ctrl/Cmd + Enter

The frontend will:
- Try to connect to the backend API first
- Show "✓ Spelling checked (API)" if connected
- Fall back to client-side checking if API unavailable
- Show "✓ Spelling checked (Client-side mode)" for offline mode

## 📚 API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference including:
- All endpoints and their parameters
- Request/response formats
- Error codes
- Integration examples (Python, JavaScript, Node.js)
- Security configuration
- Rate limiting recommendations

## 🔧 Configuration

### Backend CORS Settings

To add additional allowed origins, edit [main.py](main.py:7):

```python
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://vaporjawn.github.io",
        "http://localhost:*",
        "http://127.0.0.1:*",
        "https://your-custom-domain.com"  # Add your domains here
    ]
}})
```

### Frontend API Endpoints

To configure which API endpoints the frontend tries, edit [docs/app.js](docs/app.js):

```javascript
const API_CONFIG = {
    endpoints: [
        'https://your-production-api.com/api/check',  // Production
        'http://localhost:5000/api/check',             // Local dev
        'http://127.0.0.1:5000/api/check'             // Alternative
    ],
    timeout: 5000
};
```

## 🌐 Deployment

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-spell-checker-api

# Deploy
git push heroku master

# Test
curl https://your-spell-checker-api.herokuapp.com/api/health
```

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Deploy to Google Cloud Run

```bash
# Build and deploy
gcloud run deploy spell-checker-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🧪 Testing

### Manual Testing

1. **Test health endpoint**:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Test spell check**:
   ```bash
   curl -X POST http://localhost:5000/api/check \
     -H "Content-Type: application/json" \
     -d '{"text": "Helo wrld"}'
   ```

3. **Test error handling**:
   ```bash
   # Empty text
   curl -X POST http://localhost:5000/api/check \
     -H "Content-Type: application/json" \
     -d '{"text": ""}'
   ```

### Automated Testing

Run the test client:
```bash
python test_api_client.py
```

This will test:
- ✓ Health check endpoint
- ✓ Status endpoint
- ✓ Spell checking with correct text
- ✓ Spell checking with errors
- ✓ Error handling (empty text)
- ✓ Error handling (text too long)

## 🔍 Frontend Features

The frontend ([docs/index.html](docs/index.html) + [docs/app.js](docs/app.js)) includes:

### API Integration
- Automatic connection to backend API
- Multiple endpoint fallback
- Request timeout handling (5 seconds)
- Automatic retry logic

### Client-Side Fallback
- Works offline without API
- Basic spell checking using edit distance
- Common English words dictionary

### User Experience
- Real-time character counter
- Loading states ("Checking...")
- Success/error notifications
- Keyboard shortcuts (Ctrl/Cmd + Enter)
- Auto-resizing textarea

### Error Handling
- Network errors → fallback to client-side
- API errors → user-friendly messages
- Input validation → clear error messages

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"

**Cause**: macOS AirPlay Receiver uses port 5000

**Solutions**:
1. Disable AirPlay Receiver:
   - System Settings → General → AirDrop & Handoff
   - Turn off "AirPlay Receiver"

2. Use a different port:
   ```python
   # In main.py, change:
   if __name__ == "__main__":
       app.run(port=5001)  # Use port 5001 instead
   ```

### Issue: CORS errors in browser

**Cause**: Your origin is not in the allowed list

**Solution**: Add your origin to [main.py](main.py:7):
```python
CORS(app, resources={r"/api/*": {
    "origins": ["https://your-domain.com"]
}})
```

### Issue: "Connection refused"

**Cause**: Flask server not running

**Solution**: Start the server:
```bash
source venv/bin/activate
python main.py
```

### Issue: Frontend shows "Client-side mode"

**Cause**: Cannot connect to backend API

**Debug**:
1. Check server is running: `curl http://localhost:5000/api/health`
2. Check browser console for errors (F12)
3. Verify API endpoints in [docs/app.js](docs/app.js)

## 📊 Monitoring

### Check API Status
```bash
curl http://localhost:5000/api/status
```

Response shows component health:
```json
{
  "status": "operational",
  "components": {
    "api": "operational",
    "spell_checker": "operational",
    "cors": "enabled",
    "security_headers": "enabled"
  }
}
```

### Monitor in Production

For production deployments, consider integrating:
- **Logging**: Use application logging
- **Monitoring**: Datadog, New Relic, or similar
- **Error Tracking**: Sentry, Rollbar
- **Uptime Monitoring**: Pingdom, UptimeRobot

## 🔒 Security Best Practices

### For Development
- ✅ Already configured: Security headers
- ✅ Already configured: Input validation
- ✅ Already configured: CORS restrictions

### For Production
1. **Use HTTPS**: Always use TLS in production
2. **Rate Limiting**: Add rate limiting:
   ```bash
   pip install Flask-Limiter
   ```

3. **API Keys**: Consider adding API key authentication
4. **Monitoring**: Enable request logging
5. **Firewall**: Configure firewall rules

## 📖 Additional Resources

- **API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Main README**: [README.md](README.md)
- **GitHub Pages Setup**: [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)

## 🎯 Next Steps

1. ✅ **API is ready** - Start the server and test it
2. ✅ **Frontend is integrated** - Open docs/index.html and try it
3. 🚀 **Deploy to production** - Follow deployment guide
4. 📝 **Customize** - Modify endpoints, add features
5. 📊 **Monitor** - Set up logging and monitoring

## 💡 Tips

1. **Development**: Use `http://localhost:5001` to avoid AirPlay conflicts
2. **Testing**: Use `test_api_client.py` for automated testing
3. **Frontend**: Opens directly in browser, no server needed for client-side mode
4. **Production**: Always use HTTPS and add rate limiting
5. **CORS**: Add your production domain to allowed origins before deploying

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Vaporjawn/Spell-Checker/issues)
- **Documentation**: Check API_DOCUMENTATION.md
- **Examples**: See test_api_client.py for usage examples

---

**Ready to go!** 🎉

Start the server with `python main.py` and open `docs/index.html` to see your spell checker in action!
