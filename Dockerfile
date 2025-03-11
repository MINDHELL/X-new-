# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (not needed for Telegram bot, but useful for debugging)
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
