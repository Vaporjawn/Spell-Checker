# Deployment Guide

This guide covers deployment to both GitHub Pages (frontend) and Surge (alternative hosting).

## 📦 Deployment Options

### Option 1: GitHub Pages (Recommended for Static Frontend)

GitHub Pages is perfect for hosting the static frontend of your spell checker.

#### Setup Steps:

1. **Enable GitHub Pages**
   ```bash
   # The docs/ folder is already configured
   # Go to your repository settings on GitHub
   ```

2. **Configure Repository Settings**
   - Go to: `https://github.com/Vaporjawn/Spell-Checker/settings/pages`
   - Under "Source", select: `Deploy from a branch`
   - Choose branch: `master`
   - Select folder: `/docs`
   - Click "Save"

3. **Access Your Site**
   - Your site will be available at: `https://vaporjawn.github.io/Spell-Checker/`
   - It may take a few minutes for the first deployment

4. **Update Deployment** (After making changes)
   ```bash
   git add docs/
   git commit -m "Update frontend deployment"
   git push origin master
   ```

### Option 2: Surge (Alternative Static Hosting)

Surge provides fast, simple static hosting with custom domains.

#### Installation:

```bash
npm install -g surge
```

#### Deploy to Surge:

```bash
# Navigate to the docs directory
cd docs/

# Deploy (first time)
surge

# Follow the prompts:
# - Email: victor.williams.dev@gmail.com
# - Password: [create one]
# - Project path: [press enter to use current directory]
# - Domain: [choose a subdomain like spell-checker-vw.surge.sh]

# Update deployment (after changes)
cd docs/
surge --domain spell-checker-vw.surge.sh
```

#### Custom Domain with Surge:

```bash
# If you have a custom domain
surge --domain yourdomain.com
```

### Option 3: Backend Deployment (Flask API)

For the full Flask backend with Python spell checking:

#### Render.com (Recommended for Python):

1. Create a `render.yaml` file (already included)
2. Push to GitHub
3. Connect your repository to Render
4. Render will automatically deploy

#### Railway.app:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### PythonAnywhere:

1. Go to pythonanywhere.com
2. Create a free account
3. Upload your code
4. Configure WSGI file
5. Set up virtual environment

## 🔧 Configuration

### Update API Endpoint (if using backend)

If you deploy the Flask backend, update the API endpoint in `docs/app.js`:

```javascript
// Replace the local spell checking with API call
async function checkSpelling() {
    const text = textarea.value.trim();
    
    const response = await fetch('YOUR_BACKEND_URL/api/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    });
    
    const data = await response.json();
    textarea.value = data.corrected_text;
}
```

## 📊 Deployment Checklist

- [x] Created `docs/` folder for GitHub Pages
- [x] Added `index.html` with standalone spell checker
- [x] Added `style.css` for styling
- [x] Added `app.js` with client-side spell checking
- [ ] Push to GitHub repository
- [ ] Enable GitHub Pages in repository settings
- [ ] Test the deployed site
- [ ] (Optional) Set up custom domain

## 🚀 Quick Deploy Commands

### GitHub Pages:
```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push origin master
```

### Surge:
```bash
cd docs/ && surge
```

## 🔗 URLs

- **GitHub Pages**: `https://vaporjawn.github.io/Spell-Checker/`
- **Repository**: `https://github.com/Vaporjawn/Spell-Checker`
- **Surge** (example): `spell-checker-vw.surge.sh`

## 📝 Notes

- The `docs/` version uses client-side JavaScript for spell checking
- The full Python backend is still available in the main directory
- You can deploy both: static frontend on GitHub Pages, backend on Render/Railway
- The static version works offline after first load
- No backend required for basic functionality

## 🆘 Troubleshooting

### GitHub Pages not showing:
- Wait 5-10 minutes after first setup
- Check repository settings
- Ensure `docs/` folder is in master branch

### Surge deployment fails:
- Run `surge logout` then `surge login`
- Check internet connection
- Try a different subdomain

### Backend deployment issues:
- Check `requirements.txt` is up to date
- Ensure `Procfile` exists
- Verify Python version in `runtime.txt`

## 🎉 Success!

Your spell checker is now live! Share the link and start checking spelling!
