# Use a slim version of Python 3.14 for a smaller image size
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including app.py and index.html) into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run your application
CMD ["python", "backend.py"]
