# # Start from a Python base image
# FROM python:3.10.12

# # Install Node (change version as needed)
# RUN apt-get update && \
#     apt-get install -y curl && \
#     curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
#     apt-get install -y nodejs

# # Set the PYTHONPATH to include /app/server
# ENV PYTHONPATH /app/server

# # Set the working directory in the container
# WORKDIR /app

# # Copy local files to the container, including the React app build files
# COPY . .

# # Install necessary system dependencies
# RUN apt-get update && apt-get install -y libsystemd-dev

# # Install Python dependencies
# RUN pip install wheel uwsgi
# RUN pip install -r requirements.txt

# # Build the React app (make sure to run 'npm run build' before building the Docker image)
# RUN cd client && npm install && npm run build

# # Expose ports for backend and React app
# EXPOSE 5000
# EXPOSE 3000

# # Set the port environment variable for uwsgi to 5000
# ENV PORT 5000

# # Set the command to run your application
# CMD ["uwsgi", "--http", "0.0.0.0:${PORT}", "--chdir", "/app/server", "--wsgi-file", "app.py", "--callable", "app", "--http-timeout", "300", "--reuse-port", "--master", "--http-timeout", "86400"]  # Increase the HTTP timeout to 24 hours or adjust as needed
# # CMD ["uwsgi", "--http", "0.0.0.0:${PORT}", "--chdir", "/app/server", "--wsgi-file", "app.py", "--callable", "app", "--http-timeout", "300", "--http-timeout", "8190", "--reuse-port", "--master"]

