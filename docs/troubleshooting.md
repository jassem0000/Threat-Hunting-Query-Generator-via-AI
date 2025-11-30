# Troubleshooting Guide

## Common Installation Issues

### 1. Dependency Conflicts

**Problem**: Error messages like "Cannot install -r requirements.txt because these package versions have conflicting dependencies"

**Solution**:

1. Run the `install_deps.py` script which handles conflicts automatically:
   ```
   python install_deps.py
   ```
2. Or manually install packages with compatible versions:
   ```
   pip install httpx==0.27.0
   pip install ollama==0.5.3
   pip install python-multipart==0.0.7
   pip install requests==2.32.3
   pip install numpy==1.26.4
   ```

### 2. Missing Python Modules

**Problem**: ImportError when trying to run the application

**Solution**:

1. Ensure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```
2. Check your Python version (3.9+ required):
   ```
   python --version
   ```

### 3. Django Migration Errors

**Problem**: Errors when running `python manage.py migrate`

**Solution**:

1. Delete the db.sqlite3 file in the backend directory:
   ```
   cd backend
   del db.sqlite3
   ```
2. Run migrations again:
   ```
   python manage.py migrate
   ```

### 4. Ollama Connection Issues

**Problem**: "Connection refused" or "Service not found" errors

**Solution**:

1. Ensure Ollama is installed and running:
   - Download from https://ollama.ai/
   - Start the Ollama service
2. Pull a required model:
   ```
   ollama pull llama3.1
   ```
3. Test the connection:
   ```
   curl http://localhost:11434/api/tags
   ```

### 5. Port Already in Use

**Problem**: "Address already in use" when starting servers

**Solution**:

1. Kill processes using the ports:

   ```
   # On Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F

   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

   ```
   # On Linux/Mac
   lsof -i :8000
   kill -9 <PID>

   lsof -i :8501
   kill -9 <PID>
   ```

## Runtime Issues

### 1. Empty Query Results

**Problem**: Generated queries are empty or contain error messages

**Solution**:

1. Check if Ollama service is running:
   ```
   ollama list
   ```
2. Verify the model is available:
   ```
   ollama show llama3.1
   ```
3. Restart the backend service

### 2. Slow Query Generation

**Problem**: Long delays when generating queries

**Solution**:

1. Ensure you have sufficient system resources (8GB+ RAM recommended)
2. Check if the LLM model is fully downloaded:
   ```
   ollama list
   ```
3. Try a lighter model like `mistral`:
   ```
   ollama pull mistral
   ```

### 3. Frontend Not Connecting to Backend

**Problem**: "Connection refused" or "Network error" in the frontend

**Solution**:

1. Verify the backend is running:
   ```
   curl http://localhost:8000/api/health
   ```
2. Check firewall settings
3. Ensure both services are running on the same machine

## Docker Issues

### 1. Docker Compose Failures

**Problem**: Errors when running `docker-compose up`

**Solution**:

1. Check Docker daemon is running
2. Allocate more resources to Docker Desktop:
   - Memory: 4GB+
   - CPUs: 2+
3. Pull images manually:
   ```
   docker pull ollama/ollama:latest
   ```

### 2. Volume Mounting Issues

**Problem**: Permission errors or data not persisting

**Solution**:

1. Check Docker file permissions
2. Use absolute paths in volume mounts
3. Ensure Docker has access to your project directory

## Development Issues

### 1. Import Errors in IDE

**Problem**: Red squiggly lines under imports in your IDE

**Solution**:

1. Ensure your IDE is using the correct Python interpreter
2. Install dependencies in your IDE's environment:
   ```
   pip install -r requirements.txt
   ```
3. Refresh/restart your IDE

### 2. Database Migration Issues

**Problem**: Errors when adding new models or changing database schema

**Solution**:

1. Create new migrations:
   ```
   cd backend
   python manage.py makemigrations
   ```
2. Apply migrations:
   ```
   python manage.py migrate
   ```

## Performance Optimization

### 1. Memory Usage

**Problem**: High memory consumption

**Solution**:

1. Use lightweight models (Phi-3-mini instead of Llama 3.1)
2. Limit concurrent requests
3. Monitor resource usage with system tools

### 2. Response Time

**Problem**: Slow response from API endpoints

**Solution**:

1. Cache frequently used data
2. Optimize database queries
3. Use asynchronous processing for heavy operations

## Getting Help

If you continue to experience issues:

1. Check the console output for detailed error messages
2. Verify all prerequisites are correctly installed
3. Consult the project documentation in the `docs/` directory
4. Search for similar issues in the project's issue tracker
5. Reach out to the development team with:
   - Error messages
   - Steps to reproduce
   - System information (OS, Python version, etc.)

## Reporting Bugs

When reporting issues, please include:

1. Exact error message
2. Steps to reproduce
3. System environment (OS, Python version, etc.)
4. Expected vs. actual behavior
5. Any relevant screenshots or logs
