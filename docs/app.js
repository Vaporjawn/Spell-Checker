// Simple spell checker implementation
// This uses a basic edit distance algorithm for demonstration
// In production, you'd call your backend API

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

// Character counter
function updateCharCount() {
    const count = textarea.value.length;
    charCount.textContent = `${count} character${count !== 1 ? 's' : ''}`;
}

textarea.addEventListener('input', updateCharCount);
updateCharCount();

// Clear text function
function clearText() {
    textarea.value = '';
    updateCharCount();
    textarea.focus();
}

// Check spelling function
async function checkSpelling() {
    const text = textarea.value.trim();
    
    if (!text) {
        alert('Please enter some text to check!');
        return;
    }

    // Disable button and show loading state
    checkBtn.disabled = true;
    btnText.textContent = 'Checking...';

    // Simulate API delay for better UX
    await new Promise(resolve => setTimeout(resolve, 500));

    // Check spelling
    const correctedText = checker.checkText(text);
    textarea.value = correctedText;
    updateCharCount();

    // Re-enable button
    checkBtn.disabled = false;
    btnText.textContent = 'Check Spelling';

    // Show notification if changes were made
    if (text !== correctedText) {
        showNotification('Spelling checked and corrections applied!');
    } else {
        showNotification('No spelling errors found!');
    }
}

// Notification system
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-family: var(--font-secondary);
        font-weight: 500;
    `;
    notification.textContent = message;

    // Add animation
    const style = document.createElement('style');
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
    `;
    document.head.appendChild(style);

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Event listeners
checkBtn.addEventListener('click', checkSpelling);

// Auto-resize textarea
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Focus effect
textarea.addEventListener('focus', function() {
    this.parentElement.classList.add('focused');
});

textarea.addEventListener('blur', function() {
    this.parentElement.classList.remove('focused');
});

// Keyboard shortcut (Ctrl/Cmd + Enter to check)
textarea.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        checkSpelling();
    }
});
