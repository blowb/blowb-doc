Isso, A Commenting Server
=========================

.. index:: isso, Nginx, Postfix
   single: Docker; data container

*This Internet app uses a data container, Nginx and Postfix.*

`Isso`_ is a commenting system which can embed into a static website.

Configure DNS
-------------

Add an ``A`` record to point the domain you want to use with isso to the IP address of the server.

Configure Isso Options
----------------------

Create a directory to store isso configuration file:
::

   sudo mkdir -p $DOCKER_SHARE/isso

Download the isso example config file to ``$DOCKER_SHARE/isso``:
::

   sudo wget -O $DOCKER_SHARE/isso/isso.conf \
    https://raw.githubusercontent.com/posativ/isso/cb21af4cc57a197cbe73a63d5bd7a085ef98d85d/share/isso.conf

Now we need to edit the config file to make some changes for the isso container we will use. The
following commands switch the working directory to ``$DOCKER_SHARE/isso`` and modify some parts of
the configuration file (please replace ``isso@example.com`` with the email address you want
notification to come from and ``me@example.com`` to be the address which receives email
notification):

.. code-block:: bash
   :linenos:

   cd $DOCKER_SHARE/isso
   NOTIFICATION_FROM=isso@example.com
   NOTIFICATION_TO=me@example.com
   sudo ed isso.conf << EOF
   %s/^dbpath =.*/dbpath = \/var\/uwsgi\/comments.db
   %s/^notify =.*/notify = smtp
   %s/^port =.*/port = 25
   %s/^security =.*/security = none
   %s/^host = localhost/host = smtp-server
   %s/^from =.*/from = ${NOTIFICATION_FROM}
   %s/^to =.*/to = ${NOTIFICATION_TO}
   wq
   EOF
   unset NOTIFICATION_FROM NOTIFICATION_TO

Explanation:

  - **line 5**: modifies the path to the comments database file to a location where writable by the uWSGI process(es);

  - **line 6-11**: set the email notification to your email address using the postfix server we have configured on the
    host system.

Now we can edit this config file manually to customize it for our website:
::

   sudo $EDITOR $DOCKER_SHARE/isso/isso.conf

We probably need to modify the ``host`` option in the ``[general]`` section. Follow the instructions in the comments
above the ``host`` option to update the option to the website URL that isso will be used in. If this isso instance need
to serve multiple websites, you probably also need to look into the option ``name`` in the ``[general]`` section. We can
also customize some other options, such as ``enabled`` in the ``[moderation]`` section to turn on or off moderation,
etc.

Start the Isso Docker Container
-------------------------------

Create a data container for isso:
::

   docker run -v /var/uwsgi --name isso-data busybox /bin/true

Start the isso Docker container:
::

   docker run --restart always -d -v $DOCKER_SHARE/isso:/etc/isso:ro \
    --volumes-from isso-data --name isso \
    --env NUM_PROCESSES=1 --env NUM_THREADS=2 \
    --add-host smtp-server:$HOST_ADDR blowb/isso

The Dockerfile from which the image was generated is `available <https://hub.docker.com/r/blowb/isso/~/dockerfile/>`_.
We may adjust ``NUM_THREADS`` and ``NUM_PROCESSES`` depending on the needs, but for a small website, ``NUM_THREADS=2``
and ``NUM_PROCESSES=1`` should be good enough.

Configure Nginx
---------------

Replace ``comments.example.com`` with the domain you want to use to serve as an isso server and run
the following commands:
::

   cd $DOCKER_SHARE/nginx
   ISSO_URL='comments.example.com'
   sudo -s <<EOF
   sed -e "s/@server_name@/$ISSO_URL/g" \
    -e 's/@uwsgi_server@/isso:9000/g' uwsgi.conf.tmpl >isso.conf
   sed -e "s/@server_name@/$ISSO_URL/g" \
    -e 's/@uwsgi_server@/isso:9000/g' uwsgi.tls.conf.tmpl >isso.tls.conf
   EOF

The commands above generate two configuration files which pass all requests to the isso instance
(``comments.example.com`` in the example above) in the uWSGI protocol. Edit ``isso.tls.conf`` to
replace the dummy key and certificate with your key and certificate if you do not want to use the
dummy one.

Recreate the Nginx container:
::

   docker restart nginx


.. _Isso: http://posativ.org/isso/
