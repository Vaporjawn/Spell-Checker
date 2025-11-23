# Monitoring and Analytics Guide

## Overview

This document describes the monitoring, analytics, and observability features implemented in the Spell Checker application.

## Frontend Analytics

### Built-in Analytics System

The application includes a comprehensive client-side analytics system that tracks:

#### User Events
- **Page Load**: Application initialization and load time
- **Text Input**: User typing activity (debounced)
- **Spell Check Operations**: Initiated checks and results
- **Button Clicks**: All user interactions
- **Keyboard Shortcuts**: Shortcut usage tracking
- **Notifications**: Shown notifications and types

#### Performance Metrics
- **Spell Check Duration**: Time taken for each check operation
- **API Response Time**: Backend API performance
- **Client-side Processing**: Fallback processing time
- **Retry Attempts**: Number of retry operations

#### Error Tracking
- **API Failures**: Backend connection issues
- **Client-side Errors**: JavaScript exceptions
- **Validation Errors**: Input validation failures
- **Network Timeouts**: Request timeout tracking

### Analytics Data Structure

```javascript
{
  sessionId: "session_1234567890_abc123def",
  events: [
    {
      name: "app_loaded",
      timestamp: "2024-01-01T12:00:00.000Z",
      sessionId: "session_1234567890_abc123def",
      data: {}
    },
    {
      name: "check_spelling_started",
      timestamp: "2024-01-01T12:01:00.000Z",
      sessionId: "session_1234567890_abc123def",
      data: {
        textLength: 250,
        wordCount: 45
      }
    }
  ]
}
```

### Accessing Analytics Data

In the browser console:
```javascript
// Get all analytics data
const analytics = window.getAnalytics();
console.log(analytics);

// View specific metrics
console.log('Session ID:', analytics.sessionId);
console.log('Total Events:', analytics.events.length);
console.log('App State:', analytics.state);
```

## Backend Monitoring

### Health Check Endpoints

#### `/api/health` - Basic Health Check
Returns system health status with version information.

**Response:**
```json
{
  "status": "healthy",
  "service": "spell-checker-api",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "system": {
    "python_version": "3.11.x",
    "platform": "Linux-x86_64",
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

#### `/api/status` - Component Status
Returns detailed status of all system components.

**Response:**
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

#### `/api/metrics` - Performance Metrics
Returns application performance metrics.

**Response:**
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

## Integration with External Services

### Recommended Monitoring Services

#### 1. **Sentry** (Error Tracking)
```javascript
// Frontend integration
Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0,
});

// Send custom events
Sentry.captureMessage('Custom event', 'info');
```

#### 2. **Google Analytics 4**
```javascript
// Add to index.html
gtag('config', 'GA_MEASUREMENT_ID', {
  page_path: window.location.pathname,
});

// Track custom events
gtag('event', 'spell_check', {
  event_category: 'engagement',
  event_label: 'user_action'
});
```

#### 3. **Datadog** (Full-stack Monitoring)
```javascript
// Frontend RUM
datadogRum.init({
  applicationId: 'YOUR_APP_ID',
  clientToken: 'YOUR_CLIENT_TOKEN',
  service: 'spell-checker',
  env: 'production',
  version: '1.0.0',
  sampleRate: 100,
  trackInteractions: true,
});
```

#### 4. **New Relic** (APM)
```python
# Backend integration in main.py
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

@app.route("/api/check", methods=["POST"])
@newrelic.agent.background_task()
def api_check():
    # Your code here
    pass
```

## Custom Analytics Implementation

### Sending Analytics to Your Backend

Update `docs/app.js` to send analytics to your server:

```javascript
async function sendToAnalytics(event) {
    try {
        await fetch('/api/analytics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(event)
        });
    } catch (error) {
        console.error('Failed to send analytics:', error);
    }
}

// Modify trackEvent function
function trackEvent(eventName, eventData = {}) {
    if (!ANALYTICS.enabled) return;

    const event = {
        name: eventName,
        timestamp: new Date().toISOString(),
        sessionId: ANALYTICS.sessionId,
        data: eventData
    };

    ANALYTICS.events.push(event);

    // Send to backend
    sendToAnalytics(event);
}
```

### Backend Analytics Endpoint

Add to `main.py`:

```python
@app.route("/api/analytics", methods=["POST"])
def track_analytics():
    """Track analytics events"""
    try:
        data = request.get_json()

        # Store in database or send to analytics service
        # Example: store_event(data)

        return jsonify({
            'success': True,
            'message': 'Event tracked'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## Performance Monitoring

### Key Performance Indicators (KPIs)

Monitor these metrics for optimal performance:

1. **Response Time**
   - Target: < 500ms for API calls
   - Target: < 100ms for client-side operations

2. **Error Rate**
   - Target: < 1% of total requests
   - Critical threshold: 5%

3. **Uptime**
   - Target: 99.9% uptime
   - Track downtime incidents

4. **User Engagement**
   - Average checks per session
   - Text length distribution
   - Feature usage (keyboard shortcuts, clear button)

### Performance Budget

```javascript
// Performance thresholds
const PERFORMANCE_BUDGET = {
    firstContentfulPaint: 1800,  // ms
    largestContentfulPaint: 2500, // ms
    totalBlockingTime: 200,       // ms
    cumulativeLayoutShift: 0.1,   // score
    timeToInteractive: 3800       // ms
};
```

## Alerting and Notifications

### Recommended Alert Rules

1. **High Error Rate**
   - Condition: Error rate > 5% for 5 minutes
   - Action: Send notification to team

2. **Slow Response Time**
   - Condition: Average response time > 2 seconds for 10 minutes
   - Action: Investigate performance issue

3. **Service Down**
   - Condition: Health check fails 3 consecutive times
   - Action: Page on-call engineer

4. **Unusual Traffic**
   - Condition: Request rate > 200% of normal
   - Action: Check for DDoS or traffic spike

## Logging Best Practices

### Frontend Logging
```javascript
// Structured logging
console.log('📊 [Analytics]', {
    event: 'spell_check_completed',
    duration: 234,
    success: true
});

console.error('❌ [Error]', {
    type: 'api_failure',
    endpoint: '/api/check',
    status: 500
});
```

### Backend Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Structured logging
logger.info('Spell check request', extra={
    'text_length': len(text),
    'user_agent': request.headers.get('User-Agent'),
    'ip': request.remote_addr
})
```

## Dashboard Recommendations

### Key Metrics to Display

1. **System Health Dashboard**
   - API uptime percentage
   - Active users (current)
   - Total requests (24h)
   - Average response time
   - Error rate

2. **User Behavior Dashboard**
   - Checks per hour/day
   - Popular features
   - User retention
   - Session duration

3. **Performance Dashboard**
   - P50, P95, P99 response times
   - Slowest endpoints
   - Error breakdown
   - Resource utilization

## Privacy Considerations

### Data Collection Guidelines

1. **Anonymize Data**
   - Don't track personal information
   - Use session IDs instead of user identifiers
   - Don't log actual text content

2. **User Consent**
   - Provide opt-out mechanism
   - Clear privacy policy
   - Transparent data usage

3. **Data Retention**
   - Limit retention period
   - Automatic data cleanup
   - Comply with GDPR/CCPA

### Implementation Example

```javascript
// Respect Do Not Track
const ANALYTICS = {
    enabled: !navigator.doNotTrack || navigator.doNotTrack === "0",
    sessionId: generateSessionId(),
    events: []
};

// Opt-out function
function disableAnalytics() {
    ANALYTICS.enabled = false;
    localStorage.setItem('analytics_disabled', 'true');
}
```

## Testing Monitoring Setup

### Verify Analytics

```bash
# Open browser console and run:
# 1. Check analytics data
window.getAnalytics()

# 2. Trigger test event
trackEvent('test_event', { test: true })

# 3. Check if event was recorded
window.getAnalytics().events
```

### Verify Backend Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Status check
curl http://localhost:5000/api/status

# Metrics
curl http://localhost:5000/api/metrics
```

## Next Steps

1. **Choose Monitoring Service**: Select Sentry, Datadog, or New Relic
2. **Set Up Dashboards**: Create custom dashboards for key metrics
3. **Configure Alerts**: Set up alerting rules
4. **Document Runbooks**: Create incident response procedures
5. **Regular Reviews**: Schedule monthly monitoring reviews

## Resources

- [Sentry Documentation](https://docs.sentry.io/)
- [Google Analytics Documentation](https://developers.google.com/analytics)
- [Datadog Documentation](https://docs.datadoghq.com/)
- [New Relic Documentation](https://docs.newrelic.com/)
- [Web Vitals](https://web.dev/vitals/)

---

For questions or issues, please open a GitHub issue or contact the development team.
