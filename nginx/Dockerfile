FROM nginx

RUN apt-get install --no-install-recommends -y apache2-utils

RUN htpasswd -cBb /etc/nginx/.htpasswd admin admin

EXPOSE 80
