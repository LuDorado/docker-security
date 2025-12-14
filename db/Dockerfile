FROM postgres:15.8-alpine3.20

COPY --chown=postgres:postgres init-db/ /docker-entrypoint-initdb.d/

RUN chmod 755 /docker-entrypoint-initdb.d/ && \
    chmod 644 /docker-entrypoint-initdb.d/*

EXPOSE 5432

USER postgres
