..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Isso, A Commenting Server
=========================

`Isso`_ is a commenting system which can embed into a static website.

Configure Isso Options
----------------------

Create a directory to store isso configuration file:
::

   sudo mkdir -p $DOCKER_SHARE/isso

Download the isso example config file to ``$DOCKER_SHARE/isso``:
::

   sudo wget -O $DOCKER_SHARE/isso/isso.conf \
    https://github.com/posativ/isso/raw/c8655731d6d183a590c04bdf1f97a0afbebee822/share/isso.conf

Now we need to edit the config file to make some changes for the isso container we'll use. The
following commands switch your working directory to ``$DOCKER_SHARE/isso`` and modify some parts of
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
   %s/^host = localhost/host = docker-host
   %s/^from =.*/from = ${NOTIFICATION_FROM}
   %s/^to =.*/to = ${NOTIFICATION_TO}
   wq
   EOF
   unset NOTIFICATION_FROM NOTIFICATION_TO

Explanation:

  - **line 5**: modifies the path to the comments database file to a location where writable by the uWSGI process(es);

  - **line 6-11**: set the email notification to your email address using the postfix server we have configured on the
    host system.

Now edit this config file manually to customize it for your website:
::

   sudo $EDITOR $DOCKER_SHARE/isso/isso.conf

Modify the ``host`` option in the ``[general]`` section. Follow the instructions in the comments
above the ``host`` option to update the option to your website URL. If you need to serve multiple
websites, you probably also need to look into the option ``name`` in the ``[general]`` section. You
can also update some other options for your need, such as ``enabled`` in the ``[moderation]``
section to turn on or off moderation, etc.

Start the Isso Docker Container
-------------------------------

Create a data container for isso:
::

   docker run -v /var/uwsgi --name isso-data busybox /bin/true

Start the isso docker container:
::

   docker run --restart always -d -v $DOCKER_SHARE/isso:/etc/isso:ro --volumes-from isso-data \
    --env NUM_PROCESSES=1 --env NUM_THREADS=2 --add-host smtp-server:$DOCKER_INET \
    --name isso blowb/isso

You may adjust ``NUM_THREADS`` and ``NUM_PROCESSES`` depending on your need, but for a small
website, ``NUM_THREADS=2`` and ``NUM_PROCESSES=1`` should be enough.

Configure Nginx
---------------

First add an ``A`` record to your domain (e.g. ``comments.example.com``) pointing to the IP address
of the host system.

Replace ``comments.example.com`` with the address you want to use to serve as an isso server and run
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

The commands above generate two configuration files which pass all requests to the isso server
(``comments.example.com`` in the example above) in the uWSGI protocol. Edit ``isso.tls.conf`` to
replace the dummy key and certificate with your key and certificate if you don't want to use the
dummy one.

Add a new link to the ``nginx-links.txt`` file:
::

   echo --link isso:isso >> ~/util/nginx-links.txt

Recreate the Nginx container:
::

   ~/util/rerun-nginx.sh


.. _Isso: http://postage.org/isso/
