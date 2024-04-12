FROM python:3.12.3-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

COPY .asoundrc /root/.asoundrc

RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    libasound2-dev \
    portaudio19-dev \
    libcairo2-dev \
    libgirepository1.0-dev \
    flac

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main2.py when the container launches
CMD ["python3.12", "main2.py"]