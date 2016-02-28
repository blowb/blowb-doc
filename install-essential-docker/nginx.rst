Install Nginx
=============

.. index:: Nginx, reverse proxy

Nginx will be used to serve as a reverse proxy to forward incoming traffic to proper containers.

Create the directory to serve the configuration files and certificates on the host system:
::

   sudo mkdir -p $DOCKER_SHARE/nginx/tls

.. index:: TLS
   see: SSL; TLS

If needed create a dummy SSL/TLS key pair for Nginx:
::

    sudo openssl req -x509 -nodes -days 3000 -newkey rsa:4096 \
     -keyout $DOCKER_SHARE/nginx/tls/dummy.key \
     -out $DOCKER_SHARE/nginx/tls/dummy.crt
    sudo chmod 600 $DOCKER_SHARE/nginx/tls/dummy.key

.. index::
   single: Docker; volume

Docker volumes will be used by the Nginx container to access the web resources of some Internet apps. Since we need to
add additional Docker volumes into this container later for some Internet apps, we need to recreate this container
frequently, as each time the volumes in a Docker container changes, it is required to recreate this container. For
convenience, we create a helper script to do this:
::

   mkdir ~/util
   cat > ~/util/rerun-nginx.sh <<'EOF'
   #!/bin/bash

   echo Stoping and deleting current Nginx container...
   docker stop nginx && docker rm nginx
   echo Creating the new Nginx container...
   docker run --restart always -d -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 \
    --dns $HOST_ADDR -v $DOCKER_SHARE/nginx:/etc/nginx/conf.d:ro \
    $(cat ~/util/nginx-volumes.txt) --name nginx nginx
   EOF
   chmod +x ~/util/rerun-nginx.sh

This script stops the Nginx container and removes it (if existing), and create and run a new Nginx container with the
volumes indicated in ``~/util/nginx-volumes.txt``. Now run the this script to create the Nginx container:
::

   ~/util/rerun-nginx.sh

Also download the :doc:`template Nginx configuration files <../appendices/list-of-nginx-config>`, which we will use
later when deploying Internet apps:
::

   for f in fastcgi.conf.tmpl fastcgi.tls.conf.tmpl reverse-proxy.tls.conf.tmpl \
    redirect-https.conf.tmpl uwsgi.conf.tmpl uwsgi.tls.conf.tmpl; do
     sudo wget -O $DOCKER_SHARE/nginx/$f http://docs.blowb.org/_downloads/$f
     sudo sed -i "s/@resolver@/$HOST_ADDR/g" $DOCKER_SHARE/nginx/$f
   done
