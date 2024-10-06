# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install necessary packages
RUN pip install --upgrade pip && \
    pip install streamlit elasticsearch sentence-transformers transformers prometheus_client

# Expose the port for Streamlit
EXPOSE 8501

# Expose port for Prometheus metrics
EXPOSE 8000

# Command to run the Streamlit app
CMD ["streamlit", "run", "mainapp.py"]

