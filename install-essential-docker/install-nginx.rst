..  Copyright (C) Hong Xu <hong@topbug.net> 2015

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Install Nginx
=============

Nginx will be used to serve as a reverse proxy to forward incoming traffic to appropriate
containers.

Create the directory to serve the configuration files and certificates on the host:
::

   sudo mkdir -p $DOCKER_SHARE/nginx/tls

If needed create a dummy SSL/TLS key pair for nginx:
::

    sudo openssl req -x509 -nodes -days 3000 -newkey rsa:2048 \
     -keyout $DOCKER_SHARE/nginx/tls/dummy.key -out $DOCKER_SHARE/nginx/tls/dummy.crt
    sudo chmod 600 $DOCKER_SHARE/nginx/tls/dummy.key

Since we need to add additional links into this container later, which means we need to recreate
this container frequently, for convenience, we create a script to do this:
::

   mkdir ~/util
   cat > ~/util/rerun-nginx.sh <<'EOF'
   #!/bin/bash

   echo Stoping and deleting current Nginx container...
   docker stop nginx && docker rm nginx
   echo Creating the new Nginx container...
   docker run --restart always -d -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 \
    -v $DOCKER_SHARE/nginx:/etc/nginx/conf.d:ro $(cat ~/util/nginx-links.txt) \
    $(cat ~/util/nginx-volumes.txt) --name nginx nginx
   EOF
   chmod +x ~/util/rerun-nginx.sh

Run the script to create the Nginx container:
::

   ~/util/rerun-nginx.sh

Also download the :doc:`template Nginx configuration files <appendices/list-of-nginx-config>`:
::

   for f in uwsgi.conf.tmpl uwsgi.tls.conf.tmpl fastcgi.conf.tmpl fastcgi.tls.conf.tmpl; do
     sudo wget -O $DOCKER_SHARE/nginx/$f http://docs.blowb.org/_downloads/$f
   done
