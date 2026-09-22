# Pinned deliberately. This image was last built in March 2021 and production
# still runs the nginx 1.19.7 it shipped, so an unpinned rebuild would move
# production several years of nginx in one step, unannounced. 1.30 is the
# current stable line; bump it as a visible change with CI green.
FROM nginx:1.30.5

COPY default.conf /etc/nginx/conf.d/default.conf
