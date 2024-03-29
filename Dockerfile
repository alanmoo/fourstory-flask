# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# ENV variables
ENV PORT=80
ENV FLASK_DEBUG=false
ENV FLASK_ENV=production
ENV WORKERS=4

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE $PORT

# Define environment variable

# Run app.py when the container launches
CMD gunicorn -w $WORKERS -b 0.0.0.0:$PORT run:app