FROM python:3.8-slim

# Install PostgreSQL 17 client tools (to match Postgres:17 server)
RUN apt-get update && apt-get install -y wget gnupg lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && apt-get install -y postgresql-client-17 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python script
COPY . .

# Install only what you need directly
RUN pip install psycopg2-binary

CMD ["python", "elt_script.py"]
