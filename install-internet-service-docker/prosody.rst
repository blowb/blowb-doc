Prosody, An XMPP Communication Server
=====================================

.. index:: dnsmasq, MariaDB, OpenLDAP, Prosody, XMPP
   see: Jabber; XMPP
   see: Extensible Messaging and Presence Protocol; XMPP

*This Internet app uses dnsmasq, MariaDB and OpenLDAP.*

`Prosody`_ is a modern XMPP (the Extensible Messaging and Presence Protocol, a.k.a. Jabber) communication server, which
serves the purpose for different types of communication, such as text messaging, audio and video calls, multi-party
chatting, etc.

Configure DNS
-------------

Add an ``A`` record to point the domain to be used by Prosody to the IP address of the server.

Configure the MariaDB Database
------------------------------

Follow the instructions in :doc:`../common-tasks/add-mariadb-database` to create a new user and a database both named as
``prosody`` in the MariaDB database.

Configure the OpenLDAP Database
-------------------------------

Follow the instructions in :doc:`../common-tasks/group-tasks-openldap` to create a new group ``prosody`` and add
all users who will be granted to use Prosody to this group.

Set up Prosody
--------------

Create a directory to store Prosody configuration files:
::

   sudo mkdir -p $DOCKER_SHARE/prosody
   cd $DOCKER_SHARE/prosody
   sudo mkdir -p certs conf.d

Download the default Prosody configuration file:
::

   docker pull blowb/prosody
   sudo -s <<< "docker run --rm blowb/prosody cat /etc/prosody/prosody.cfg.lua > prosody.cfg.lua"

The Dockerfile from which the image was generated is `available
<https://hub.docker.com/r/blowb/prosody/~/dockerfile/>`_.

Run the following commands to modify the default configuration file to adjust it for running inside a Docker container,
after replacing ``dc=example,dc=com`` with the ``LDAP_SUFFIX`` value in :doc:`../install-essential-docker/openldap`, and
``PASSWORD`` with the password of the user ``prosody`` in MariaDB we have just created:

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

  - **line 3**: use the OpenLDAP server we have set up for authentication instead of the internal one;
  - **line 4**: specify the base in the LDAP database;
  - **line 5**: specify the OpenLDAP server;
  - **line 6**: use ``uid`` attribute as the user name;
  - **line 7**: use the SQL backend for data storage;
  - **line 9-10**: specify MariaDB connection parameters.

We can edit the configuration file and enable additional modules as we need, such as ``carbons`` for message
synchronization, ``mam_sql`` for message archiving, etc.

Copy the XMPP server certificate into ``$DOCKER_SHARE/prosody/certs``. If a dummy key and certificate will be used
instead of a valid certificate, run the following command to generate a pair of dummy keys, similar to the key
generation described in :doc:`../install-essential-docker/nginx`:
::

   sudo mkdir -p $DOCKER_SHARE/prosody/certs
   sudo openssl req -x509 -nodes -days 3000 -newkey rsa:4096 \
    -keyout $DOCKER_SHARE/prosody/certs/dummy.key \
    -out $DOCKER_SHARE/prosody/certs/dummy.crt

Add a virtual host configuration files after replacing ``example.com`` with the domain to be used as the XMPP domain,
which is the domain that will appear in the user names in the form of ``someone@example.com``. Note that this domain is
not necessarily the same as the domain which the server uses for the DNS query for its IP address. Also, optionally we
can replace ``dummy.crt`` and ``dummy.key`` with a different pair of certification and key:
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

We can create additional configuration host configurations if more than one domains will be hosted.

To start the container:
::

   docker run -d -t --restart always --dns $HOST_ADDR \
    -v $DOCKER_SHARE/prosody/prosody.cfg.lua:/etc/prosody/prosody.cfg.lua:ro \
    -v $DOCKER_SHARE/prosody/conf.d:/etc/prosody/conf.d:ro \
    -v $DOCKER_SHARE/prosody/certs:/etc/prosody/certs:ro \
    --name prosody -p 5222:5222 -p 5223:5223 -p 5269:5269 -p 5298:5298 \
    blowb/prosody

.. _`Prosody`: http://prosody.im
