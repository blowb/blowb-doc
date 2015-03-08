Install Nginx
=============

Nginx will be used to serve as a reverse proxy to forward incoming traffic to appropriate
containers.

Create the directory to serve the configuration files and certificates on the host:
::

   sudo mkdir -p /var/docker/nginx/ssl

If needed create a dummy SSL/TLS key pair for nginx:
::

    sudo openssl req -x509 -nodes -days 3000 -newkey rsa:2048 \
     -keyout /var/docker/nginx/ssl/dummy.key -out /var/docker/nginx/ssl/dummy.crt
    sudo chmod 600 /var/docker/nginx/ssl/dummy.key

Create the nginx container and run:
::

   docker run --restart always -d -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 \
    -v /var/docker/nginx:/etc/nginx/conf.d --name nginx nginx
