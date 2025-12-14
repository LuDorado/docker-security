FROM postgres:15.8-alpine3.20

# Copy initialization scripts with proper ownership
COPY --chown=postgres:postgres init-db/ /docker-entrypoint-initdb.d/

# Set proper permissions for init scripts
RUN chmod 755 /docker-entrypoint-initdb.d/ && \
    chmod 644 /docker-entrypoint-initdb.d/*

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} || exit 1

# Expose port
EXPOSE 5432

# Use default postgres user (already non-root in postgres image)
USER postgres
