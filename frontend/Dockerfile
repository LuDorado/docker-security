FROM nginx:1.26.2-alpine3.20

RUN addgroup -g 1001 -S nginxuser && \
    adduser -u 1001 -D -S -G nginxuser nginxuser

COPY --chown=nginxuser:nginxuser nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginxuser:nginxuser index.html /usr/share/nginx/html/
COPY --chown=nginxuser:nginxuser style.css /usr/share/nginx/html/
COPY --chown=nginxuser:nginxuser app.js /usr/share/nginx/html/
COPY --chown=nginxuser:nginxuser images/ /usr/share/nginx/html/images/
COPY --chown=nginxuser:nginxuser favicon.ico /usr/share/nginx/html/

RUN chmod -R 644 /usr/share/nginx/html/* && \
    chmod 755 /usr/share/nginx/html/images && \
    chmod 644 /etc/nginx/nginx.conf && \
    chown -R nginxuser:nginxuser /var/cache/nginx && \
    chown -R nginxuser:nginxuser /var/log/nginx && \
    chown -R nginxuser:nginxuser /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown nginxuser:nginxuser /var/run/nginx.pid

EXPOSE 80

USER nginxuser

CMD ["nginx", "-g", "daemon off;"]
