FROM python:latest

# Set dash debug mode
ENV DASH_DEBUG_MODE False

# Set the working directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the scripts to the folder
COPY . /app

# Start the server
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "main:server"]
