FROM appertly/nginx-rewrite

COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
