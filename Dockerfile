# Use the official Python image as a base
FROM python:3.9-slim-buster


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]