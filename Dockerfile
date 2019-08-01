# Use an official Python runtime as a parent image
FROM registry.redhat.io/ubi8/python-36

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV VERSION "0.3"

# Run app.py when the container launches
CMD ["python", "app.py"]
