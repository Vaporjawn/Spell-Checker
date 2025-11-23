// Enhanced spell checker implementation
// Features: Error handling, retry logic, loading states, monitoring, and UX improvements
// This uses both backend API and client-side fallback

// Configuration
const API_CONFIG = {
    // Try these endpoints in order: production, local dev, fallback to client-side
    endpoints: [
        // Add your production URL here when deployed (e.g., Heroku, Railway, etc.)
        // 'https://your-app.herokuapp.com/api/check',
        'http://localhost:5000/api/check', // Local development
        'http://127.0.0.1:5000/api/check'  // Alternative local
    ],
    timeout: 5000, // 5 second timeout per endpoint
    maxRetries: 3,
    retryDelay: 1000 // 1 second between retries
};

// Analytics and monitoring configuration
const ANALYTICS = {
    enabled: true,
    sessionId: generateSessionId(),
    events: []
};

// Generate unique session ID for analytics
function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// Track analytics events
function trackEvent(eventName, eventData = {}) {
    if (!ANALYTICS.enabled) return;

    const event = {
        name: eventName,
        timestamp: new Date().toISOString(),
        sessionId: ANALYTICS.sessionId,
        data: eventData
    };

    ANALYTICS.events.push(event);
    console.log('📊 Analytics:', event);

    // In production, send to analytics service
    // sendToAnalytics(event);
}

// Error tracking
function trackError(error, context = {}) {
    const errorInfo = {
        message: error.message || String(error),
        stack: error.stack,
        context: context,
        timestamp: new Date().toISOString(),
        sessionId: ANALYTICS.sessionId,
        userAgent: navigator.userAgent
    };

    console.error('❌ Error tracked:', errorInfo);

    // In production, send to error tracking service (e.g., Sentry)
    // sendToErrorTracking(errorInfo);
}

// Performance monitoring
const PERF_MONITOR = {
    marks: {},

    start(label) {
        this.marks[label] = performance.now();
    },

    end(label) {
        if (!this.marks[label]) return null;
        const duration = performance.now() - this.marks[label];
        delete this.marks[label];

        trackEvent('performance_metric', {
            label: label,
            duration: Math.round(duration),
            unit: 'ms'
        });

        return duration;
    }
};

class SpellChecker {
    constructor() {
        // Common English words dictionary (subset for demo)
        this.dictionary = new Set([
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            'is', 'was', 'are', 'been', 'has', 'had', 'were', 'said', 'did', 'having',
            'may', 'should', 'am', 'being', 'able', 'might', 'must', 'shall', 'can', 'could',
            'write', 'something', 'here', 'spell', 'checked', 'checking', 'text', 'word', 'words',
            'hello', 'world', 'test', 'example', 'sample', 'demo', 'correct', 'wrong', 'right',
            'spelling', 'grammar', 'language', 'english', 'document', 'file', 'content'
        ]);
    }

    // Calculate edit distance between two strings
    editDistance(s1, s2) {
        const m = s1.length;
        const n = s2.length;
        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (s1[i - 1] === s2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.min(
                        dp[i - 1][j] + 1,
                        dp[i][j - 1] + 1,
                        dp[i - 1][j - 1] + 1
                    );
                }
            }
        }

        return dp[m][n];
    }

    // Find the closest matching word in dictionary
    correct(word) {
        const lowerWord = word.toLowerCase();

        // If word is in dictionary, return as-is
        if (this.dictionary.has(lowerWord)) {
            return word;
        }

        // Find closest match
        let minDistance = Infinity;
        let bestMatch = word;

        for (const dictWord of this.dictionary) {
            const distance = this.editDistance(lowerWord, dictWord);
            if (distance < minDistance) {
                minDistance = distance;
                bestMatch = dictWord;
            }
        }

        // Only suggest if distance is reasonable (≤2 edits)
        if (minDistance <= 2) {
            // Preserve original capitalization pattern
            if (word[0] === word[0].toUpperCase()) {
                bestMatch = bestMatch.charAt(0).toUpperCase() + bestMatch.slice(1);
            }
            return bestMatch;
        }

        return word;
    }

    // Check entire text
    checkText(text) {
        const words = text.split(/(\s+)/); // Split but keep whitespace
        return words.map(word => {
            // Only check actual words, not whitespace
            if (word.trim() && /[a-zA-Z]/.test(word)) {
                return this.correct(word);
            }
            return word;
        }).join('');
    }
}

// Initialize spell checker
const checker = new SpellChecker();

// DOM elements
const textarea = document.getElementById('input');
const charCount = document.getElementById('charCount');
const checkBtn = document.getElementById('checkBtn');
const btnText = document.getElementById('btnText');
const btnIcon = checkBtn.querySelector('.btn-icon');

// State management
const APP_STATE = {
    isChecking: false,
    lastCheckTime: null,
    totalChecks: 0,
    errors: [],
    mode: 'idle' // idle, checking, error, success
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    trackEvent('app_loaded', {
        timestamp: new Date().toISOString()
    });
});

// Initialize application
function initializeApp() {
    updateCharCount();
    setupEventListeners();
    showHelpTooltip();
    checkBackendHealth();
}

// Setup all event listeners
function setupEventListeners() {
    // Character counter
    textarea.addEventListener('input', updateCharCount);

    // Check button
    checkBtn.addEventListener('click', checkSpelling);

    // Auto-resize textarea
    textarea.addEventListener('input', autoResizeTextarea);

    // Focus effects
    textarea.addEventListener('focus', handleFocus);
    textarea.addEventListener('blur', handleBlur);

    // Keyboard shortcuts
    textarea.addEventListener('keydown', handleKeyboardShortcuts);

    // Track user interactions
    textarea.addEventListener('input', debounce(() => {
        trackEvent('user_typing', { length: textarea.value.length });
    }, 2000));
}

// Auto-resize textarea
function autoResizeTextarea() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
}

// Handle focus
function handleFocus() {
    this.parentElement.classList.add('focused');
    trackEvent('textarea_focused');
}

// Handle blur
function handleBlur() {
    this.parentElement.classList.remove('focused');
}

// Keyboard shortcuts handler
function handleKeyboardShortcuts(e) {
    // Ctrl/Cmd + Enter to check
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        checkSpelling();
        trackEvent('keyboard_shortcut_used', { key: 'check_spelling' });
    }

    // Ctrl/Cmd + K to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        clearText();
        trackEvent('keyboard_shortcut_used', { key: 'clear_text' });
    }
}

// Debounce utility
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show help tooltip on first visit
function showHelpTooltip() {
    const hasSeenHelp = localStorage.getItem('hasSeenHelp');
    if (!hasSeenHelp) {
        setTimeout(() => {
            showNotification('💡 Tip: Press Ctrl+Enter (or Cmd+Enter) to check spelling quickly!', 'info', 5000);
            localStorage.setItem('hasSeenHelp', 'true');
        }, 2000);
    }
}

// Check backend health
async function checkBackendHealth() {
    try {
        const healthEndpoints = API_CONFIG.endpoints.map(ep =>
            ep.replace('/api/check', '/api/health')
        );

        for (const endpoint of healthEndpoints) {
            try {
                const response = await fetch(endpoint, {
                    method: 'GET',
                    signal: AbortSignal.timeout(2000)
                });

                if (response.ok) {
                    console.log('✅ Backend API is healthy:', endpoint);
                    trackEvent('backend_health_check', {
                        status: 'healthy',
                        endpoint: endpoint
                    });
                    return true;
                }
            } catch (e) {
                // Continue to next endpoint
            }
        }

        console.log('⚠️ Backend API not available - will use client-side fallback');
        trackEvent('backend_health_check', { status: 'unavailable' });
        return false;
    } catch (error) {
        trackError(error, { context: 'health_check' });
        return false;
    }
}

// Character counter
function updateCharCount() {
    const count = textarea.value.length;
    const maxLength = 10000;
    const percentage = (count / maxLength) * 100;

    charCount.textContent = `${count.toLocaleString()} / ${maxLength.toLocaleString()} characters`;

    // Visual feedback for character limit
    if (percentage > 90) {
        charCount.style.color = '#f5576c';
        charCount.style.fontWeight = '600';
    } else if (percentage > 75) {
        charCount.style.color = '#f093fb';
        charCount.style.fontWeight = '500';
    } else {
        charCount.style.color = '';
        charCount.style.fontWeight = '';
    }
}

// Clear text function
function clearText() {
    if (!textarea.value.trim()) {
        showNotification('Text is already empty', 'info', 2000);
        return;
    }

    const confirmed = textarea.value.length > 100 ?
        confirm('Are you sure you want to clear all text?') : true;

    if (confirmed) {
        textarea.value = '';
        updateCharCount();
        textarea.focus();
        trackEvent('text_cleared', { length: textarea.value.length });
        showNotification('✓ Text cleared', 'success', 2000);
    }
}

// Check spelling function with enhanced error handling and loading states
async function checkSpelling() {
    const text = textarea.value.trim();

    if (!text) {
        showNotification('⚠️ Please enter some text to check!', 'warning');
        trackEvent('check_spelling_empty');
        return;
    }

    // Check text length
    const maxLength = 10000;
    if (text.length > maxLength) {
        showNotification(`⚠️ Text too long! Maximum ${maxLength.toLocaleString()} characters allowed.`, 'error');
        trackEvent('check_spelling_too_long', { length: text.length });
        return;
    }

    // Prevent multiple simultaneous checks
    if (APP_STATE.isChecking) {
        showNotification('⏳ Already checking... please wait', 'info', 2000);
        return;
    }

    // Start performance monitoring
    PERF_MONITOR.start('spell_check');

    // Update state
    APP_STATE.isChecking = true;
    APP_STATE.mode = 'checking';
    APP_STATE.totalChecks++;

    // Show loading state
    setLoadingState(true);

    try {
        trackEvent('check_spelling_started', {
            textLength: text.length,
            wordCount: text.split(/\s+/).length
        });

        // Try backend API first with retry logic
        const result = await retryOperation(
            () => checkWithBackend(text),
            API_CONFIG.maxRetries
        );

        // Update textarea with corrected text
        textarea.value = result.correctedText;
        updateCharCount();

        // Calculate metrics
        const duration = PERF_MONITOR.end('spell_check');
        const hasChanges = text !== result.correctedText;

        trackEvent('check_spelling_completed', {
            mode: result.mode,
            hasChanges: hasChanges,
            duration: duration,
            endpoint: result.endpoint || 'client-side'
        });

        // Show success notification
        if (hasChanges) {
            const changeCount = countChanges(text, result.correctedText);
            showNotification(
                `✓ ${changeCount} correction${changeCount !== 1 ? 's' : ''} applied! (${result.mode})`,
                'success'
            );
        } else {
            showNotification(`✓ No spelling errors found! (${result.mode})`, 'success');
        }

        APP_STATE.mode = 'success';
        APP_STATE.lastCheckTime = Date.now();

    } catch (error) {
        console.error('Spell check failed:', error);
        trackError(error, {
            context: 'spell_check',
            textLength: text.length
        });

        // Fallback to client-side checking
        console.log('Using client-side spell checker as fallback');

        try {
            const correctedText = checker.checkText(text);
            textarea.value = correctedText;
            updateCharCount();

            const duration = PERF_MONITOR.end('spell_check');
            const hasChanges = text !== correctedText;

            trackEvent('check_spelling_fallback', {
                hasChanges: hasChanges,
                duration: duration
            });

            if (hasChanges) {
                const changeCount = countChanges(text, correctedText);
                showNotification(
                    `✓ ${changeCount} correction${changeCount !== 1 ? 's' : ''} applied (Client-side mode)`,
                    'warning'
                );
            } else {
                showNotification('✓ No spelling errors found! (Client-side mode)', 'success');
            }

            APP_STATE.mode = 'success';

        } catch (fallbackError) {
            console.error('Client-side fallback failed:', fallbackError);
            trackError(fallbackError, { context: 'client_side_fallback' });

            showNotification(
                '❌ Unable to check spelling. Please try again or refresh the page.',
                'error',
                5000
            );

            APP_STATE.mode = 'error';
            APP_STATE.errors.push({
                timestamp: Date.now(),
                error: fallbackError.message
            });
        }
    } finally {
        // Always restore button state
        setLoadingState(false);
        APP_STATE.isChecking = false;
    }
}

// Set loading state with visual feedback
function setLoadingState(isLoading) {
    checkBtn.disabled = isLoading;

    if (isLoading) {
        btnText.textContent = 'Checking...';
        checkBtn.classList.add('loading');

        // Animate button icon (spinning)
        if (btnIcon) {
            btnIcon.style.animation = 'spin 1s linear infinite';
        }

        // Show progress indicator
        showProgressIndicator();
    } else {
        btnText.textContent = 'Check Spelling';
        checkBtn.classList.remove('loading');

        // Stop animation
        if (btnIcon) {
            btnIcon.style.animation = '';
        }

        // Hide progress indicator
        hideProgressIndicator();
    }
}

// Show progress indicator
function showProgressIndicator() {
    let progressBar = document.getElementById('progressBar');

    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.id = 'progressBar';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            z-index: 9999;
            transition: width 0.3s ease;
        `;
        document.body.appendChild(progressBar);
    }

    // Animate progress
    progressBar.style.width = '0%';
    setTimeout(() => { progressBar.style.width = '30%'; }, 100);
    setTimeout(() => { progressBar.style.width = '60%'; }, 500);
    setTimeout(() => { progressBar.style.width = '80%'; }, 1500);
}

// Hide progress indicator
function hideProgressIndicator() {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBar.remove();
        }, 300);
    }
}

// Count changes between original and corrected text
function countChanges(original, corrected) {
    const originalWords = original.split(/\s+/);
    const correctedWords = corrected.split(/\s+/);
    let changes = 0;

    for (let i = 0; i < Math.min(originalWords.length, correctedWords.length); i++) {
        if (originalWords[i] !== correctedWords[i]) {
            changes++;
        }
    }

    return changes;
}

// Retry operation with exponential backoff
async function retryOperation(operation, maxRetries = 3, baseDelay = 1000) {
    let lastError;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            lastError = error;

            if (attempt < maxRetries - 1) {
                const delay = baseDelay * Math.pow(2, attempt);
                console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms...`);

                trackEvent('retry_attempt', {
                    attempt: attempt + 1,
                    maxRetries: maxRetries,
                    delay: delay
                });

                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    throw lastError;
}

// Check with backend API
async function checkWithBackend(text) {
    // Try each endpoint until one succeeds
    for (const endpoint of API_CONFIG.endpoints) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.success && data.corrected !== undefined) {
                console.log(`✓ Connected to backend API: ${endpoint}`);
                return {
                    correctedText: data.corrected,
                    mode: 'API',
                    endpoint: endpoint
                };
            } else {
                throw new Error(data.error || 'Invalid response from server');
            }
        } catch (error) {
            console.log(`✗ Failed to connect to ${endpoint}:`, error.message);
            // Continue to next endpoint
        }
    }

    // If all endpoints failed, throw error to trigger client-side fallback
    throw new Error('All backend endpoints failed');
}

// Notification system with enhanced styling and options
function showNotification(message, type = 'success', duration = 3000) {
    // Define colors based on notification type
    const colors = {
        success: 'linear-gradient(135deg, #667eea, #764ba2)',
        warning: 'linear-gradient(135deg, #f093fb, #f5576c)',
        error: 'linear-gradient(135deg, #ff6b6b, #ee5a6f)',
        info: 'linear-gradient(135deg, #4facfe, #00f2fe)'
    };

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification-toast';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.success};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-family: var(--font-secondary);
        font-weight: 500;
        max-width: 400px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    `;

    // Add icon based on type
    const icon = getNotificationIcon(type);
    const iconSpan = document.createElement('span');
    iconSpan.textContent = icon;
    iconSpan.style.fontSize = '1.25rem';

    const messageSpan = document.createElement('span');
    messageSpan.textContent = message;

    notification.appendChild(iconSpan);
    notification.appendChild(messageSpan);

    // Add close button for longer notifications
    if (duration > 3000) {
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '×';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            margin-left: auto;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        closeBtn.onclick = () => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        };
        notification.appendChild(closeBtn);
    }

    // Ensure animation styles exist
    if (!document.getElementById('notification-animations')) {
        const style = document.createElement('style');
        style.id = 'notification-animations';
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
            @keyframes spin {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }
            .notification-toast:hover {
                transform: scale(1.02);
                transition: transform 0.2s ease;
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Track notification
    trackEvent('notification_shown', {
        type: type,
        message: message.substring(0, 50)
    });

    // Remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Get icon for notification type
function getNotificationIcon(type) {
    const icons = {
        success: '✓',
        warning: '⚠️',
        error: '❌',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

// Event listeners
checkBtn.addEventListener('click', checkSpelling);

// Auto-resize textarea (legacy support)
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Focus effect (legacy support)
textarea.addEventListener('focus', function() {
    this.parentElement.classList.add('focused');
});

textarea.addEventListener('blur', function() {
    this.parentElement.classList.remove('focused');
});

// Keyboard shortcut (Ctrl/Cmd + Enter to check) - legacy support
textarea.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        checkSpelling();
    }
});

// Export analytics data (for debugging)
window.getAnalytics = function() {
    return {
        sessionId: ANALYTICS.sessionId,
        events: ANALYTICS.events,
        state: APP_STATE
    };
};

// Visibility change tracking
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        trackEvent('page_hidden');
    } else {
        trackEvent('page_visible');
    }
});

// Before unload tracking
window.addEventListener('beforeunload', function() {
    trackEvent('session_ended', {
        duration: Date.now() - (ANALYTICS.events[0]?.timestamp ? new Date(ANALYTICS.events[0].timestamp).getTime() : Date.now()),
        totalChecks: APP_STATE.totalChecks,
        errors: APP_STATE.errors.length
    });
});
