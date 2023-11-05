# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /BANCO_FINAL

# Copy the requirements file into the container
COPY requeriments.txt /BANCO_FINAL/

# Install the required dependencies
RUN pip install -r requeriments.txt

# Copy the current directory contents into the container
COPY . /BANCO_FINAL/

# Expose the port that your Django application will run on (not necessary for connecting to the database)
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]