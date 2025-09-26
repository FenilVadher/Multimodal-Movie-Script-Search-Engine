# 🚀 Deploy to Render - Complete Guide

## **Step 1: Push Code to GitHub**

```bash
# From your project root
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

## **Step 2: Create Render Account**

1. Go to **[render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub**
4. Authorize Render to access your repositories

## **Step 3: Deploy Backend (API)**

1. **Click "New +" → "Web Service"**
2. **Connect your repository**: `Multimodal-Movie-Script-Search-Engine`
3. **Configure the service**:
   - **Name**: `movie-search-api`
   - **Environment**: `Python 3`
   - **Build Command**: `cd fullstack-movie-search/Multimodal-Movie-Script-Search-Engine/backend && pip install -r requirements.txt`
   - **Start Command**: `cd fullstack-movie-search/Multimodal-Movie-Script-Search-Engine/backend && python app_fixed.py`
   - **Plan**: `Free`

4. **Add Environment Variables**:
   - `FLASK_ENV` = `production`
   - `PORT` = `10000` (Render will set this automatically)

5. **Click "Create Web Service"**

## **Step 4: Deploy Frontend**

1. **Click "New +" → "Static Site"**
2. **Connect the same repository**
3. **Configure the static site**:
   - **Name**: `movie-search-frontend`
   - **Build Command**: `cd fullstack-movie-search/Multimodal-Movie-Script-Search-Engine/frontend && npm install && npm run build`
   - **Publish Directory**: `fullstack-movie-search/Multimodal-Movie-Script-Search-Engine/frontend/build`

4. **Click "Create Static Site"**

## **Step 5: Update Frontend API URL**

Once your backend is deployed, you'll get a URL like:
`https://movie-search-api.onrender.com`

Update your frontend API configuration:

```typescript
// In frontend/src/services/api.ts
const API_BASE_URL = 'https://movie-search-api.onrender.com/api';
```

## **🎉 Your App Will Be Live At:**

- **Backend API**: `https://movie-search-api.onrender.com`
- **Frontend**: `https://movie-search-frontend.onrender.com`

## **✅ Features That Will Work:**

- 🔍 **Movie Search**: Search by dialogue, scene, keywords
- 🎭 **Famous Quotes**: "Why so serious?", "All is well", etc.
- 📝 **Text Summarization**: AI-powered content analysis
- 🎬 **Script Generation**: Generate movie scripts and dialogues
- 📱 **Mobile Responsive**: Works on all devices
- ⚡ **Fast Performance**: Optimized for production

## **🔧 Troubleshooting:**

### **If Backend Build Fails:**
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### **If Frontend Build Fails:**
- Check for TypeScript errors
- Add `GENERATE_SOURCEMAP=false` to build command
- Verify all npm dependencies are installed

### **If API Calls Fail:**
- Update the API_BASE_URL in frontend
- Check CORS configuration in Flask app
- Verify backend is running and accessible

## **💡 Pro Tips:**

1. **Free Tier Limitations**:
   - Backend may sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds to wake up
   - 750 hours/month free (enough for development)

2. **Performance Optimization**:
   - Keep your backend active with a simple ping service
   - Use environment variables for configuration
   - Monitor usage in Render dashboard

3. **Custom Domain** (Optional):
   - Add your own domain in Render settings
   - Configure DNS records
   - Get automatic SSL certificates

**Ready to deploy? Let's push to GitHub first! 🚀**
