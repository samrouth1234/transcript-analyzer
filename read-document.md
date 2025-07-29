1, What is def `__init__` in Python?

- In Python, the `__init__` method is known as the initializer method.
- It is automatically called when you create a new instance of a class.
- It allows you to define custom behaviors that set up an object's initial state, such as defining attributes or performing specific actions at the moment of object creation.

2, What is def in Python ?

- in python def is a keyword used to define a function

  - function are reusable blocks of code designed to perform a specific task .
  - they allow for modularity , reusable , and improved organization within a program.

- Syntax :

```pycon
    def function_name(parameter1, parameter2, ...):
    """Docstring: Optional, describes what the function does."""
    # Function body: code to be executed when the function is called
    # ...
    return result # Optional: returns a value from the function
```

3, what is to_dict() in Python ?

- in python def is a keyword used to define a function
- `to_dict()` converts a Pandas DataFrame into a dictionary.
- The structure of the resulting dictionary depends on the specified orientation, allowing you to choose how rows and columns are represented
- This method offers flexibility in how the DataFrame data is structured within the resulting dictionary through the orient parameter.
- Different orient values produce different dictionary formats, allowing users to tailor the output to their specific needs.

4, what is `DataFrame` in python ?

- DataFrame is a two-dimensional, labeled data structure with columns of potentially different types, primarily used within the pandas library.
- It can be thought of as a table, similar to a spreadsheet or a SQL table.

# YouTube Transcript API - Deployment Fixes

## Issues Fixed

### 1. Flask App Configuration

- ✅ Updated `app.py` to use proper host and port configuration for deployment
- ✅ Added environment variable support for PORT
- ✅ Configured Flask app with proper static and template folder paths

### 2. Vercel Configuration

- ✅ Updated `vercel.json` with proper version and environment settings
- ✅ Added static file routing for CSS/JS assets
- ✅ Added PYTHONPATH environment variable

### 3. CORS Configuration

- ✅ Updated CORS to allow all origins for deployment
- ✅ Proper CORS headers for API endpoints

### 4. Error Handling

- ✅ Added comprehensive error handling in transcript service
- ✅ Added logging for better debugging in production
- ✅ Added timeout for external API calls
- ✅ Added health check endpoint

### 5. Code Fixes

- ✅ Fixed typo in `helpers.py` ('youth.be' → 'youtu.be')
- ✅ Added proper exception handling with custom messages
- ✅ Added request validation

### 6. Deployment Files

- ✅ Added `runtime.txt` for Python version specification
- ✅ Added `.vercelignore` to exclude unnecessary files
- ✅ Added `Procfile` for deployment compatibility
- ✅ Updated `requirements.txt` with gunicorn

## How to Deploy

### Option 1: Vercel (Recommended)

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

### Option 2: Heroku

1. Create Heroku app: `heroku create your-app-name`
2. Add Python buildpack: `heroku buildpacks:set heroku/python`
3. Deploy: `git push heroku main`

### Option 3: Railway

1. Connect your GitHub repo to Railway
2. Deploy automatically on push

## Testing Your Deployment

1. Run the test script: `python test_deployment.py`
2. Or manually test these endpoints:
   - Health check: `GET /api/v1/health`
   - Transcript: `POST /api/v1/transcript` with `{"url": "youtube_url"}`

## Environment Variables (if needed)

- `PORT`: Port number for the application (default: 5000)
- `FLASK_ENV`: Set to 'production' for production deployment

## Common Issues and Solutions

### Issue: "Module not found" errors

**Solution**: Ensure your `vercel.json` has the PYTHONPATH environment variable set.

### Issue: Static files not loading

**Solution**: Check that your `vercel.json` has proper static file routing.

### Issue: CORS errors

**Solution**: The CORS configuration has been updated to allow all origins.

### Issue: Timeout errors

**Solution**: Added timeout configurations for external API calls.

### Issue: YouTube API rate limiting

**Solution**: The app now handles multiple language attempts and provides better error messages.

## Monitoring

- Check Vercel function logs in the Vercel dashboard
- Use the health check endpoint to monitor service status
- Monitor error logs for debugging

## Support

If you encounter issues:

1. Check the Vercel function logs
2. Test the health endpoint
3. Verify your YouTube URLs are valid
4. Check if the video has available transcripts
