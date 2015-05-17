..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Prosody, An XMPP Communication Server
=====================================

`Prosody`_ is a modern XMPP (the Extensible Messaging and Presence Protocol) communication server, which serves the
purpose for communication, e.g. text messaging, audio and video calls, multi-party chatting, etc.

Configure DNS
-------------

Please add an A record to point the domain you want to use with Prosody to the IP address of the server.

Configure the MariaDB Database
------------------------------

Please follow the instructions in :doc:`../common-tasks/add-mariadb-database` to create a new user and a database both
named as ``prosody`` in MariaDB.

Configure the OpenLDAP Database
-------------------------------

Please follow the instructions in :doc:`../common-tasks/group-tasks-openldap` to create a new group ``prosody`` and add
all users which will be granted to use this service to this group.

Set up Prosody
--------------

Create a directory to store Prosody configuration files:
::

   sudo mkdir -p $DOCKER_SHARE/prosody
   cd $DOCKER_SHARE/prosody
   sudo mkdir -p certs conf.d

Download the default prosody configuration file:
::

   docker pull blowb/prosody
   sudo -s <<< "docker run --rm blowb/prosody cat /etc/prosody/prosody.cfg.lua > prosody.cfg.lua"

Run the following command to modify the default config file to adjust it to run a Docker container, after replacing
'dc=example,dc=com' with the ``LDAP_SUFFIX`` value in :doc:`../install-essential-docker/openldap`, and ``PASSWORD`` with
the password of the prosody user in MariaDB you've just created:

.. code-block:: bash
   :linenos:

   LDAP_SUFFIX='dc=example,dc=com'
   sudo sed -ri \
    -e 's/(authentication = )\"internal_plain\"/\1\"ldap\"/' \
    -e "1s/^/ldap_base = \"ou=people,$LDAP_SUFFIX\"\n/" \
    -e '1s/^/ldap_server = \"ldap\"\n/' \
    -e "1s/^/ldap_filter = \"(\&(uid=\$user) (memberOf=cn=prosody,ou=groups,$LDAP_SUFFIX))\"\n/" \
    -e 's/\-\-(storage = \"sql\")/\1/' \
    prosody.cfg.lua
   sudo sed -i '/^storage = "sql"/a\
    sql = { driver = "MySQL", database = "prosody", username = "prosody", password = "PASSWORD", host = "db" }' \
    prosody.cfg.lua


Explanation:

  - **line 3**: use the OpenLDAP server we set up for authentication instead of the internal one;
  - **line 4**: specify the base in the LDAP database;
  - **line 5**: specify the OpenLDAP server;
  - **line 6**: use ``uid`` attribute as the user name;
  - **line 7**: use sql backend for data storage;
  - **line 9-10**: specify MariaDB connection parameters.

You can edit the configuration file and enable additional modules if you want, such as ``carbons`` for message
synchronization, ``mam_sql`` for message archiving, etc.

Put your XMPP server certificate in ``$DOCKER_SHARE/prosody/certs``. If you just want to use a dummy key, run the
following command to copy the dummy key we generated in :doc:`../install-essential-docker/nginx`:
::

   sudo cp $DOCKER_SHARE/nginx/tls/dummy.* $DOCKER_SHARE/prosody/certs/

Add a virtual host configuration files after replacing ``example.com`` with your domain, and replace ``dummy.crt`` and
``dummy.key`` with your certification and key if you have one:
::

   MY_DOMAIN=example.com
   sudo -s <<EOF
   cat > conf.d/myhost.cfg.lua <<EEOOFF
   VirtualHost "$MY_DOMAIN"

       ssl = {
                   key = "/etc/prosody/certs/dummy.key";
                   certificate = "/etc/prosody/certs/dummy.crt";
       }
   EEOOFF
   EOF

You can create additional configuration host configurations if you need to host more than one domain.

To start the container:
::

   docker run -d -t --restart always --dns $DOCKER_ADDR \
    -v $DOCKER_SHARE/prosody/prosody.cfg.lua:/etc/prosody/prosody.cfg.lua:ro \
    -v $DOCKER_SHARE/prosody/conf.d:/etc/prosody/conf.d:ro \
    -v $DOCKER_SHARE/prosody/certs:/etc/prosody/certs:ro \
    --name prosody -p 5222:5222 -p 5223:5223 -p 5269:5269 -p 5298:5298 \
    blowb/prosody

.. _`Prosody`: http://prosody.im
