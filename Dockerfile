# Use a lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .

# Install only required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]
