FROM nginx

COPY default.conf /etc/nginx/conf.d/default.conf
COPY *.map /etc/nginx/conf.d/
