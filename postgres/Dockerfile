# Use the official PostgreSQL 16 image
FROM postgres:16

# Install required dependencies and pgvector extension
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-16 \
    git \
    make \
    gcc \
    && git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector && make && make install \
    && rm -rf pgvector
