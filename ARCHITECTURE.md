# Frontend-Backend Integration Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        GitHub Pages                              │
│                  https://vaporjawn.github.io/                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                Frontend (docs/)                         │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │    │
│  │  │  index.html  │  │   style.css  │  │   app.js   │  │    │
│  │  │              │  │              │  │            │  │    │
│  │  │  - UI        │  │  - Design    │  │  - Logic   │  │    │
│  │  │  - Structure │  │  - Theme     │  │  - API     │  │    │
│  │  │  - Layout    │  │  - Animation │  │  - Fallback│  │    │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP POST /api/check
                              │ (tries multiple endpoints)
                              ▼
        ┌─────────────────────────────────────────┐
        │      Backend API Endpoints              │
        │                                         │
        │  1. Production (Railway/Heroku)        │
        │     https://your-app.up.railway.app    │
        │                                         │
        │  2. Local Development                  │
        │     http://localhost:5000              │
        │                                         │
        │  3. Alternative Local                  │
        │     http://127.0.0.1:5000             │
        └─────────────────────────────────────────┘
                              │
                              │ If all fail
                              ▼
        ┌─────────────────────────────────────────┐
        │    Client-Side Fallback Algorithm       │
        │                                         │
        │  - Built-in dictionary                 │
        │  - Edit distance algorithm             │
        │  - Works offline                       │
        └─────────────────────────────────────────┘
```

## Request Flow Diagram

```
┌─────────────┐
│   Browser   │
│   (User)    │
└──────┬──────┘
       │
       │ 1. Enter text
       │ 2. Click "Check Spelling"
       ▼
┌──────────────────────────────────────┐
│     Frontend JavaScript (app.js)      │
│                                      │
│  async function checkSpelling() {   │
│    try {                            │
│      // Try backend API              │
│      await checkWithBackend(text)   │
│    } catch {                        │
│      // Fallback to client-side     │
│      checker.checkText(text)        │
│    }                                │
│  }                                  │
└──────┬───────────────────────────────┘
       │
       │ 3. POST request with JSON
       │    { "text": "..." }
       ▼
┌──────────────────────────────────────┐
│    Try Endpoint 1 (Production)       │
│    Timeout: 5 seconds                │
└──────┬───────────────────────────────┘
       │
       ├─ Success ──┐
       │            │
       └─ Failed ───┼───► Try Endpoint 2 (Local)
                    │     Timeout: 5 seconds
                    │            │
                    │            ├─ Success ──┐
                    │            │            │
                    │            └─ Failed ───┼───► Try Endpoint 3
                    │                         │            │
                    │                         │            ├─ Success ──┐
                    │                         │            │            │
                    │                         │            └─ Failed ───┼───► Client-Side
                    │                         │                         │
                    ▼                         ▼                         ▼
            ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
            │   Backend    │        │   Backend    │        │  Client-Side │
            │   Response   │        │   Response   │        │   Algorithm  │
            └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
                   │                       │                       │
                   └───────────────────────┴───────────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │   Return Corrected Text │
                              └────────────┬────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │   Update UI & Notify    │
                              │                         │
                              │  ✓ Backend: "Checked!"  │
                              │  ✓ Fallback: "Offline"  │
                              └─────────────────────────┘
```

## Backend API Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Flask Backend (main.py)                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │           CORS Configuration                      │    │
│  │  Origins: GitHub Pages, localhost                │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Security Headers                        │    │
│  │  - X-Frame-Options: DENY                         │    │
│  │  - Content-Security-Policy                       │    │
│  │  - Strict-Transport-Security                     │    │
│  └──────────────────────────────────────────────────┘    │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │           API Endpoints                           │    │
│  │                                                   │    │
│  │  GET  /api/health                                │    │
│  │       → { status: "healthy" }                    │    │
│  │                                                   │    │
│  │  POST /api/check                                 │    │
│  │       Request: { text: "..." }                   │    │
│  │       ↓                                          │    │
│  │       1. Validate input                          │    │
│  │       2. Check length (max 10,000)              │    │
│  │       3. Call Checker.correct()                  │    │
│  │       4. Return corrections                      │    │
│  │       ↓                                          │    │
│  │       Response: {                                │    │
│  │         success: true,                           │    │
│  │         original: "...",                         │    │
│  │         corrected: "...",                        │    │
│  │         has_corrections: bool                    │    │
│  │       }                                          │    │
│  └──────────────────────────────────────────────────┘    │
│                          ↓                                │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Checker Class (lib/checker.py)         │    │
│  │                                                   │    │
│  │  - Trained ML model                              │    │
│  │  - Word probability calculations                 │    │
│  │  - Unigram/Bigram/Trigram analysis              │    │
│  │  - Edit distance algorithm                       │    │
│  │  - Context-aware corrections                     │    │
│  └──────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌────────────────────────────────────────────────────────────────┐
│                    Frontend Data Flow                          │
└────────────────────────────────────────────────────────────────┘

User Input: "teh quik brown fox"
     ↓
app.js: checkSpelling()
     ↓
     ├─► Try Backend API
     │        ↓
     │   POST /api/check
     │   { text: "teh quik brown fox" }
     │        ↓
     │   ┌─────────────────────────────────┐
     │   │  Backend Processing:            │
     │   │                                 │
     │   │  Split: ["teh", "quik", ...]   │
     │   │  Correct each word:            │
     │   │    "teh" → "the"               │
     │   │    "quik" → "quick"            │
     │   │    "brown" → "brown" (ok)      │
     │   │    "fox" → "fox" (ok)          │
     │   │  Join: "the quick brown fox"   │
     │   └─────────────────────────────────┘
     │        ↓
     │   Response:
     │   {
     │     success: true,
     │     original: "teh quik brown fox",
     │     corrected: "the quick brown fox",
     │     has_corrections: true
     │   }
     │
     └─► On Failure: Client-Side Fallback
              ↓
         checker.checkText(text)
              ↓
         Use built-in dictionary
         and edit distance algorithm
              ↓
         Return corrected text

Result: "the quick brown fox"
     ↓
Display in textarea
     ↓
Show notification: "✓ Spelling checked!"
```

## Error Handling Flow

```
┌────────────────────────────────────────┐
│     Robust Error Handling              │
└────────────────────────────────────────┘

Backend API Call
     ↓
┌────────────────────────────────┐
│  Possible Errors:              │
│                                │
│  1. Network timeout (5 sec)   │
│  2. Server unreachable        │
│  3. CORS error                │
│  4. Invalid JSON response     │
│  5. HTTP error (4xx, 5xx)     │
└────────────────────────────────┘
     ↓
All handled by try/catch
     ↓
Automatic fallback to client-side
     ↓
User never sees error
     ↓
Always gets corrected text
     ↓
Notification indicates mode:
  - Backend: "✓ Checked!"
  - Fallback: "✓ Checked (offline)"
```

## Deployment Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     Production Deployment                      │
└────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   GitHub Repository  │         │   Hosting Platform   │
│   Vaporjawn/         │         │   (Railway/Heroku)   │
│   Spell-Checker      │         │                      │
└──────────┬───────────┘         └──────────┬───────────┘
           │                                 │
           │ Push to master                  │
           ▼                                 │
┌──────────────────────┐                    │
│  GitHub Actions      │                    │
│  .github/workflows/  │                    │
│  deploy-pages.yml    │                    │
└──────────┬───────────┘                    │
           │                                 │
           │ Build & Deploy                  │
           ▼                                 │
┌──────────────────────┐                    │
│   GitHub Pages       │◄───────────────────┘
│   Static Frontend    │      API calls
│   HTML/CSS/JS        │
└──────────────────────┘

URL: https://vaporjawn.github.io/Spell-Checker/
     │
     └─► Calls backend API at configured endpoints
         Falls back to client-side if unavailable
```

## Security Layers

```
┌────────────────────────────────────────────────────────────────┐
│                      Security Architecture                     │
└────────────────────────────────────────────────────────────────┘

Frontend Security:
  ├─ Input sanitization
  ├─ Client-side validation
  └─ HTTPS only (GitHub Pages)

Backend Security:
  ├─ CORS restrictions (whitelisted origins)
  ├─ Input validation (length, format)
  ├─ Rate limiting ready (future)
  ├─ Security headers
  │   ├─ X-Frame-Options: DENY
  │   ├─ X-Content-Type-Options: nosniff
  │   ├─ Content-Security-Policy
  │   └─ Strict-Transport-Security
  └─ Session security
      ├─ HTTPOnly cookies
      ├─ Secure cookies
      └─ SameSite: Lax

Data Security:
  ├─ No data persistence
  ├─ Stateless API
  └─ No user tracking
```

## Performance Optimization

```
┌────────────────────────────────────────────────────────────────┐
│                   Performance Features                         │
└────────────────────────────────────────────────────────────────┘

Frontend:
  ├─ Minimal dependencies (vanilla JS)
  ├─ Async API calls (non-blocking)
  ├─ 5-second timeout per endpoint
  ├─ Client-side caching (dictionary in memory)
  └─ Lightweight payload (JSON only)

Backend:
  ├─ Pre-trained model (no training on each request)
  ├─ Efficient algorithms (edit distance)
  ├─ Input length limits (max 10,000 chars)
  └─ Stateless design (horizontal scaling ready)

Network:
  ├─ Multiple endpoint fallback
  ├─ Timeout protection
  ├─ CORS preflight optimization
  └─ CDN delivery (GitHub Pages)
```

---

**Legend:**
- `┌─┐` = System boundary
- `│` = Connection
- `↓` = Data flow direction
- `►` = Alternative path
- `├─` = Branch/Option
- `└─` = End of branch

**Last Updated**: November 23, 2025
**Author**: Victor Williams
