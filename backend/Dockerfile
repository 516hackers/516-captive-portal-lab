FROM python:3.9-alpine

WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    build-base \
    linux-headers \
    pkgconf \
    hostapd \
    dnsmasq \
    iptables \
    wireless-tools

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Copy application
COPY . .

# Create non-root user
RUN adduser -D portaluser
RUN chown -R portaluser:portaluser /app
USER portaluser

EXPOSE 5000

CMD ["python", "app.py"]
