FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && \
apt-get install --no-install-recommends --no-install-suggests -y http_rewrite_module
