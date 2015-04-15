Piwik, A Web Analytics Platform
===============================

First, please add an A record to point the domain you want to use with Piwik to the IP address of the server.

Set up MariaDB
--------------

Please follow the instructions in :doc:`../common-tasks/add-mariadb-database` to create a new user and a database both
named as ``piwik`` in MariaDB.

Set up Piwik Container
----------------------

Create a data container for Piwik:
::

   docker run -v /var/www/piwik --name piwik-data busybox /bin/true

To start the Piwik container, run the following command:
::

   docker run -d --restart always --name piwik --link mariadb:db --volumes-from piwik-data blowb/piwik

For the first time the container starts will download and decompress the Piwik installation to ``/var/www/piwik``.

Set up Nginx
------------

Now run the following command to set up Nginx, after replacing ``piwik.example.com`` with your Piwik domain:
::

   echo --link piwik:piwik >> ~/util/nginx-links.txt
   echo --volumes-from piwik-data >> ~/util/nginx-volumes.txt
   cd $DOCKER_SHARE/nginx
   PIWIK_URL='piwik.example.com'
   sudo -s <<EOF
   sed -e "s/@server_name@/$PIWIK_URL/g" \
    -e 's/@root@/piwik/g' \
    -e 's/@fastcgi_server@/piwik:9000/g' fastcgi.conf.tmpl >piwik.conf
   sed -e "s/@server_name@/$PIWIK_URL/g" \
    -e 's/@root@/piwik/g' \
    -e 's/@fastcgi_server@/piwik:9000/g' fastcgi.tls.conf.tmpl >piwik.tls.conf
   EOF

Restart the Nginx container:
::

   ~/util/rerun-nginx.sh

Configure Piwik
---------------

Visit your Piwik setup in a browser (e.g. ``https://piwik.example.com``), and follow the instructions to set up
Piwik. In the database setup page, remember in our setup, the database server is ``db``, database login is ``piwik``,
database password is the one we generated earlier, database name is ``piwik``. The table prefix can be any thing, even
empty.
