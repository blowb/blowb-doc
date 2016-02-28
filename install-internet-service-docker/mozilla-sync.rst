Firefox Sync Server, Synchronizing Firefox Across Devices
=========================================================

.. index:: Mozilla, Firefox, Nginx, MariaDB, dnsmasq
   single: Firefox Sync; Server

*This Internet app uses dnsmasq, MariaDB and Nginx.*

`Firefox Sync Server`_ is an Internet app which synchronizes Firefox (e.g. bookmarks, history, etc) across devices. By
default, Firefox uses the sync server deployed by Mozilla, but Mozilla has also released the sync server software which
we can use on our own servers for Firefox synchronization.

*Note that the setup here makes uses of the Mozilla hosted accounts server at https://accounts.firefox.com .*

Configure DNS
-------------

Store the domain we will use for the Firefox Sync Server (remember to replace ``msync.example.com`` with your domain
name):
::

   MY_DOMAIN=msync.example.com

We will use ``MY_DOMAIN`` to refer to the domain name that we will use in shell commands through this section.

Also add an ``A`` record that points the domain to the IP address of the server.

Configure the MariaDB Database
------------------------------

Follow the instructions in :doc:`../common-tasks/add-mariadb-database` to create a new user and a database both named as
``msync`` in the MariaDB database.

Configure Firefox Sync Server
-----------------------------

Create a directory for the Firefox Sync Server:
::

   sudo mkdir $DOCKER_SHARE/msync
   cd $DOCKER_SHARE/msync

Pull the Firefox Sync Server image and generate the default configuration file:
::

   docker pull blowb/mozilla-sync-server
   sudo -s <<< "docker run --rm blowb/mozilla-sync-server \
    cat /var/uwsgi/syncserver.ini > syncserver.ini"

The Dockerfile from which the image was generated is `available
<https://hub.docker.com/r/blowb/mozilla-sync-server/~/dockerfile/>`_.

Modify the default configuration file by running the following command, after replacing ``PASSWORD`` with the password
that has been set for the ``msync`` user in the MariaDB database:

.. code-block:: bash
   :linenos:

   sudo sed -ri \
    -e "s/^(public_url = ).*\$/\1https:\/\/$MY_DOMAIN/" \
    -e 's/#sqluri =.*$/sqluri = pymysql:\/\/msync:PASSWORD@db\/msync/' \
    syncserver.ini

Explanation:

  - **line 2**: set the public url that we will serve at;
  - **line 3**: set up the SQL database connection to the database we have just created earlier in `Configure the
    MariaDB Database`_ .

Start the Firefox Sync Server container:
::

   docker run -d --restart always --name msync --dns $HOST_ADDR \
    --env NUM_PROCESSES=1 --env NUM_THREADS=2 \
    -v $DOCKER_SHARE/msync/syncserver.ini:/etc/syncserver.ini:ro \
    blowb/mozilla-sync-server

We may adjust ``NUM_THREADS`` and ``NUM_PROCESSES`` depending on the needs, but for a small amount of users,
``NUM_THREADS=2`` and ``NUM_PROCESSES=1`` should be good enough.

Configure Nginx
---------------

Run the following command to generate a configuration file which would make Nginx pass all requests to the Sync Server
URL to the Firefox Sync Server container under the uWSGI protocol:
::

   cd $DOCKER_SHARE/nginx
   sudo -s <<EOF
   sed -e "s/@server_name@/$MY_DOMAIN/g" \
    redirect-https.conf.tmpl > msync.conf
   sed -e "s/@server_name@/$MY_DOMAIN/g" \
    -e 's/@uwsgi_server@/msync:9000/g' uwsgi.tls.conf.tmpl > msync.tls.conf
   EOF

Note here we do not use the http version as it is insecure to transfer users' data such as bookmarks, browsing
histories, etc. in plain text over the Internet. Edit the ``msync.tls.conf`` file to replace dummy key and certificate
if you want to use a different key and certificate.

Restart the Nginx container:
::

   docker restart nginx

Configure Firefox
-----------------

Before we start configuring, if the dummy key is used, we need to add a security exception in Firefox. Visit the URL
``https://msync.example.com`` in Firefox, where ``msync.example.com`` is the Firefox Sync Server domain. In the "Your
connection is not secure" page, click the ``Advanced`` button and then the ``Add Exception...`` button. Make sure the
``Permanently store this exception`` is checked, then click the ``Confirm Security Exception`` button.

To make Firefox uses the synchronize server we have just set up, first log out the Mozilla account if logged in, and
then type ``about:config`` in the navigation bar and press ``Enter``. If a button with the text ``I'll be careful, I
promise!`` shows up, click on it. Now you should be at a page with a list of options and a search bar on the top. Use
the search bar to search for ``services.sync.tokenServerURI``, and change the value of this option to
``https://msync.example.com/token/1.0/sync/1.5``, where ``msync.example.com`` should be replaced by the domain name of
the Firefox Sync Server, similar to what is shown in :numref:`mozilla-sync-firefox`. Now logging in the Firefox account
should make Firefox use the synchronize server we have just set up.

.. _mozilla-sync-firefox:

.. figure:: mozilla-sync-firefox.png
   :alt: Configure Firefox

   Configure Firefox to use our own server.

Verify Whether the Setup Works
------------------------------

To verify the setup works, we can see if the database has added new records for our Firefox browsers. Run the following
commands on the server:
::

   ne mariadb
   # Now inside the MariaDB container
   mysql -u root msync -p

Enter the password and run the following SQL query in the MariaDB shell:

.. code-block:: sql

   select * from users;

If a non-empty table is displayed, then the setup was likely to be successfully done.

Press ``Ctrl-D`` twice to exit to the host bash shell.

In addition, we also can check the log to see whether there are any issues:
::

   docker logs msync

Disable New Users Signups
-------------------------

After everyone we want to serve have logged in with their Firefox browsers, we may not want new users to sign up in the
server. To disable new users signups, edit ``$DOCKER_SHARE/msync/syncserver.ini`` to uncomment the ``allow_new_user =
false`` line, or run the following command:
::

   sudo sed -ri 's/^# (allow_new_users = false)/\1/' \
    $DOCKER_SHARE/msync/syncserver.ini

Restart both the ``msync`` and ``nginx`` Docker containers to apply the change:
::

   docker restart msync nginx

.. _Firefox Sync Server: https://github.com/mozilla-services/syncserver
