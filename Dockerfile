# Stage 1: Install dependencies and run tests
ARG BUILD_STAGE=builder
FROM python:3.8.19 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set FLASK_APP environment variable and run database migrations
RUN export FLASK_APP=/app/core/server.py && \
    flask db upgrade -d /app/core/migrations/ || true

# Run tests
RUN pytest --disable-warnings -q 

# Stage 2: Build final image if tests pass
FROM python:3.8.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /app /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set FLASK_APP environment variable and run database migrations
RUN export FLASK_APP=/app/core/server.py && \
    rm /app/core/store.sqlite3 && \
    flask db upgrade -d /app/core/migrations/

# Expose port and define entrypoint
EXPOSE 7755
CMD ["sh", "run.sh"]
