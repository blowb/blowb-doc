Prosody, An XMPP Communication Server
=====================================

*Uses dnsmasq, MariaDB and OpenLDAP*

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

The Dockerfile from which the image was generated is `available
<https://registry.hub.docker.com/u/blowb/prosody/dockerfile/>`_.

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

Put your XMPP server certificate in ``$DOCKER_SHARE/prosody/certs``. If you just want to use a dummy key, similar to the
key generation described in :doc:`../install-essential-docker/nginx`, run the following command to generate a pair of
dummy keys:
::

   sudo mkdir -p $DOCKER_SHARE/prosody/certs
   sudo openssl req -x509 -nodes -days 3000 -newkey rsa:4096 \
    -keyout $DOCKER_SHARE/prosody/certs/dummy.key \
    -out $DOCKER_SHARE/prosody/certs/dummy.crt

Add a virtual host configuration files after replacing ``example.com`` with the domain to be used as the XMPP domain,
which is the domain that will appear in the user names in the form of ``someone@example.com``. Note that this domain is
not necessarily the same as the domain which the server uses for the DNS query for its IP address. Also, replace
``dummy.crt`` and ``dummy.key`` with your certification and key if you have one:
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

   docker run -d -t --restart always --dns $HOST_ADDR \
    -v $DOCKER_SHARE/prosody/prosody.cfg.lua:/etc/prosody/prosody.cfg.lua:ro \
    -v $DOCKER_SHARE/prosody/conf.d:/etc/prosody/conf.d:ro \
    -v $DOCKER_SHARE/prosody/certs:/etc/prosody/certs:ro \
    --name prosody -p 5222:5222 -p 5223:5223 -p 5269:5269 -p 5298:5298 \
    blowb/prosody

.. _`Prosody`: http://prosody.im
