# Multi-stage Dockerfile for GuardNode IoT Full-Stack System
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Install system dependencies (libpcap for Scapy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, trained models, and demo telemetry data
COPY backend/ ./backend/
COPY models/ ./models/
COPY data/demo/ ./data/demo/

# Copy compiled frontend from builder
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
