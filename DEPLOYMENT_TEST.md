# Vercel Deployment Test Guide

## Steps to Deploy and Test

1. **Deploy to Vercel:**
   ```bash
   # Make sure you're in the project root directory
   vercel --prod
   ```

2. **Test the Deployment:**
   - Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
   - Try logging in with these test credentials:
     - **Principal:** username: `principal`, password: `principal123`
     - **Teacher:** username: `teacher1`, password: `teacher123`

3. **Test API Endpoints:**
   - `/api/user` - Should return current user info
   - `/api/students` - Should return list of students (requires login)
   - `/` - Should redirect to login page

4. **Common Issues and Solutions:**

   **Issue:** "Module not found" errors
   - **Solution:** Make sure all dependencies are in `backend/requirements.txt`

   **Issue:** "File not found" errors
   - **Solution:** Check that JSON files exist in the backend directory

   **Issue:** "500 Internal Server Error"
   - **Solution:** Check Vercel logs for specific error messages

5. **Check Vercel Logs:**
   - Go to your Vercel dashboard
   - Click on your project
   - Go to "Functions" tab to see serverless function logs

## Files Modified for Vercel Deployment:

1. `vercel.json` - Updated to use correct entry point
2. `backend/vercel_app.py` - Created WSGI entry point
3. `backend/app_vercel.py` - Updated file paths and logging
4. `backend/requirements.txt` - Added gunicorn dependency

## Expected Behavior:

- ✅ Application loads without errors
- ✅ Login page displays correctly
- ✅ Authentication works
- ✅ API endpoints respond correctly
- ✅ Static files (CSS/JS) load properly
- ✅ Templates render correctly

If you encounter any specific errors, please share the error message from the Vercel logs. 