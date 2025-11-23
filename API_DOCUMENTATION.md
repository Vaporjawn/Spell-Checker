# Spell Checker API Documentation

## Overview

The Spell Checker API provides endpoints for spell checking text, health monitoring, and system status.

**Base URL**: `http://localhost:5000` (development) or your deployed URL

## Authentication

Currently, no authentication is required. CORS is enabled for:
- `https://vaporjawn.github.io`
- `http://localhost:*`
- `http://127.0.0.1:*`

## Endpoints

### 1. Check Spelling

**Endpoint**: `POST /api/check`

**Description**: Check and correct spelling in provided text.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "text": "Your text to check"
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "original": "Helo wrld",
  "corrected": "Hello world",
  "has_corrections": true
}
```

**Error Responses**:

*400 Bad Request* - No text provided:
```json
{
  "success": false,
  "error": "No text provided"
}
```

*400 Bad Request* - Empty text:
```json
{
  "success": false,
  "error": "Empty text provided"
}
```

*400 Bad Request* - Text too long:
```json
{
  "success": false,
  "error": "Text too long! Maximum 10000 characters allowed."
}
```

*500 Internal Server Error*:
```json
{
  "success": false,
  "error": "Server error: [error details]"
}
```

**Example Usage**:

```bash
# Using curl
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "Helo wrld! Ths is a tst."}'

# Using JavaScript fetch
fetch('http://localhost:5000/api/check', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ text: 'Helo wrld' })
})
  .then(response => response.json())
  .then(data => console.log(data));

# Using Python requests
import requests

response = requests.post(
    'http://localhost:5000/api/check',
    json={'text': 'Helo wrld'}
)
print(response.json())
```

### 2. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check API health and system information.

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "spell-checker-api",
  "version": "1.0.0",
  "timestamp": "2025-11-23T16:34:33.616493Z",
  "system": {
    "python_version": "3.13.2",
    "platform": "macOS-26.2-arm64",
    "uptime": "available"
  },
  "endpoints": {
    "check": "/api/check",
    "health": "/api/health",
    "metrics": "/api/metrics",
    "status": "/api/status"
  }
}
```

**Example Usage**:
```bash
curl http://localhost:5000/api/health
```

### 3. Metrics

**Endpoint**: `GET /api/metrics`

**Description**: Get application metrics (for monitoring integration).

**Success Response** (200 OK):
```json
{
  "success": true,
  "metrics": {
    "total_requests": "tracked_in_production",
    "avg_response_time": "tracked_in_production",
    "error_rate": "tracked_in_production",
    "uptime": "tracked_in_production"
  },
  "note": "Integrate with monitoring service for detailed metrics"
}
```

### 4. Status

**Endpoint**: `GET /api/status`

**Description**: Check component status.

**Success Response** (200 OK):
```json
{
  "success": true,
  "status": "operational",
  "components": {
    "api": "operational",
    "spell_checker": "operational",
    "cors": "enabled",
    "security_headers": "enabled"
  },
  "timestamp": "current"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production deployments.

## CORS Configuration

The API allows cross-origin requests from:
- GitHub Pages: `https://vaporjawn.github.io`
- Local development: `http://localhost:*` and `http://127.0.0.1:*`

To add additional origins, update the CORS configuration in [main.py](main.py:7):

```python
CORS(app, resources={r"/api/*": {"origins": ["https://your-domain.com"]}})
```

## Security Headers

All responses include the following security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'`

## Validation Rules

### Text Input
- **Required**: Yes
- **Type**: String
- **Max Length**: 10,000 characters
- **Min Length**: 1 character (after trimming)

## Error Handling

All endpoints return JSON responses with a `success` field:
- `success: true` - Operation completed successfully
- `success: false` - Operation failed (check `error` field for details)

## Integration Examples

### Frontend Integration

See [docs/app.js](docs/app.js) for a complete frontend integration example that includes:
- API endpoint fallback (tries multiple endpoints)
- Client-side fallback for offline mode
- Error handling and user notifications
- Request timeout handling

### Python Integration

```python
import requests

class SpellCheckerClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def check_spelling(self, text):
        """Check spelling of text."""
        response = requests.post(
            f"{self.base_url}/api/check",
            json={"text": text}
        )
        return response.json()

    def health_check(self):
        """Check API health."""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()

# Usage
client = SpellCheckerClient()
result = client.check_spelling("Helo wrld")
print(result)
```

### Node.js Integration

```javascript
const axios = require('axios');

class SpellCheckerClient {
  constructor(baseURL = 'http://localhost:5000') {
    this.baseURL = baseURL;
  }

  async checkSpelling(text) {
    try {
      const response = await axios.post(`${this.baseURL}/api/check`, {
        text: text
      });
      return response.data;
    } catch (error) {
      throw new Error(`Spell check failed: ${error.message}`);
    }
  }

  async healthCheck() {
    const response = await axios.get(`${this.baseURL}/api/health`);
    return response.data;
  }
}

// Usage
const client = new SpellCheckerClient();
client.checkSpelling('Helo wrld').then(result => console.log(result));
```

## Running the API

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://127.0.0.1:5000`

### Production

For production deployment, use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Testing

### Using curl

```bash
# Health check
curl http://localhost:5000/api/health

# Spell check
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "test text"}'

# Status check
curl http://localhost:5000/api/status
```

### Using the Frontend

1. Start the Flask server: `python main.py`
2. Open [docs/index.html](docs/index.html) in your browser
3. The frontend will automatically connect to the API at `http://localhost:5000`

## Troubleshooting

### CORS Errors
If you encounter CORS errors, ensure your origin is listed in the CORS configuration in [main.py](main.py:7).

### Connection Refused
Make sure the Flask server is running: `python main.py`

### 400 Bad Request
- Verify the request body is valid JSON
- Ensure the `text` field is present and not empty
- Check that text length is under 10,000 characters

### 500 Internal Server Error
Check server logs for detailed error information.

## Support

For issues or questions:
- Open an issue: [GitHub Issues](https://github.com/Vaporjawn/Spell-Checker/issues)
- Check existing documentation: [README.md](README.md)
