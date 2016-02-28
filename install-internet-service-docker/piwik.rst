Piwik, A Web Analytics Platform
===============================

*This Internet app uses dnsmasq, MariaDB, Nginx and OpenLDAP.*

`Piwik`_ is a free and open source web analytics platform which can be self-hosted.

Configure DNS
-------------

Add an ``A`` record to point the domain to be used by Piwik to the IP address of the server.

Configure the MariaDB Database
------------------------------

Follow the instructions in :doc:`../common-tasks/add-mariadb-database` to create a new user and a database both named as
``piwik`` in the MariaDB database.

Set up Piwik Container
----------------------

Create a data container for Piwik:
::

   docker run -v /var/www/piwik --name piwik-data busybox /bin/true

To start the Piwik container, run the following command:
::

   docker run -d --restart always --name piwik --dns $HOST_ADDR \
    --volumes-from piwik-data blowb/piwik

The Dockerfile from which the image was generated is `available <https://hub.docker.com/r/blowb/piwik/~/dockerfile/>`_.
For the first time the container starts will download and decompress Piwik to ``/var/www/piwik``.

Configure Nginx
---------------

Now run the following command to set up Nginx, after replacing ``piwik.example.com`` with the domain of the Piwik
instance:
::

   echo --volumes-from piwik-data >> ~/util/nginx-volumes.txt
   cd $DOCKER_SHARE/nginx
   PIWIK_URL='piwik.example.com'
   sudo -s <<EOF
   sed -e "s/@server_name@/$PIWIK_URL/g" \
    -e 's/@root@/piwik/g' \
    -e 's/@fastcgi_server@/piwik:9000/g' fastcgi.conf.tmpl > piwik.conf
   sed -e "s/@server_name@/$PIWIK_URL/g" \
    -e 's/@root@/piwik/g' \
    -e 's/@fastcgi_server@/piwik:9000/g' fastcgi.tls.conf.tmpl > piwik.tls.conf
   EOF

Optionally we can edit ``piwik.tls.conf`` to use a different TLS/SSL key instead of the dummy key.

Recreate and restart the Nginx container:
::

   ~/util/rerun-nginx.sh

Configure Piwik
---------------

Visit the Piwik instance in a browser (e.g. ``https://piwik.example.com``), and follow the instructions to set up Piwik.
In the database setup page, according to our setup, the database server is ``db``, database login is ``piwik``, database
password is the one we generated earlier, and the database name is ``piwik``. The table prefix can be any thing, even
empty.

Use Piwik with OpenLDAP
-----------------------

It is optional to use Piwik with OpenLDAP. If you decide not to use Piwik with OpenLDAP, you may skip this part.

Follow the instructions in :doc:`../common-tasks/group-tasks-openldap` to create a new group ``piwik`` and add all users
who will be granted to use Piwik to this group.

First we need to install the `LoginLdap plugin <https://plugins.piwik.org/LoginLdap>`_ . To install the plugin, log into
the admin account of the Piwik instance, click the ``Administration`` link on the top right corner and then click the
``Marketplace`` link. We should now be able to see an interface similar to :numref:`piwik-marketplace`.

.. _piwik-marketplace:

.. figure:: piwik/piwik-marketplace.png
   :alt: Piwik Marketplace

   Navigate to Piwik Marketplace.

Then in the searchbox, search for ``LoginLdap``, and we should now see the LoginLdap plugin in the plugin panel as shown
in :numref:`piwik-marketplace-ldaplogin`.

.. _piwik-marketplace-ldaplogin:

.. figure:: piwik/piwik-marketplace-ldaplogin.png
   :alt: Search for LdapLogin Plugin in Piwik Marketplace

   Search for LdapLogin in Piwik Marketplace.

After that, click on the ``install`` link to install the plugin. If the installation is successful, we can click on the
``Activate`` link to activate the plugin. Alternatively, we may follow the `Piwik plugin installation guide
<https://piwik.org/faq/plugins/#faq_21>`_ and `LoginLdap installation guide
<https://github.com/piwik/plugin-LoginLdap#installation>`_ to install and activate the LoginLdap plugin.

After activating the LoginLdap plugin, we should be able to see an ``LDAP`` link in the administration panel as shown in
:numref:`piwik-ldap`.

.. _piwik-ldap:

.. figure:: piwik/piwik-ldap.png
   :alt: Piwik LdapLogin Settings

   Configure the LdapLogin plugin.

Click the link, then a list of LDAP settings should be available on the right, as shown in :numref:`piwik-ldap`. Make
sure the LDAP server settings are similar to the settings in :numref:`piwik-ldap-server`, (replace ``dc=example,ec=com``
with the ``$LDAP_SUFFIX`` in :doc:`../install-essential-docker/openldap` in the "Base DN" field) and then click
``Save``.

.. _piwik-ldap-server:

.. figure:: piwik/piwik-ldap-server.png
   :alt: Piwik LdapLogin LDAP Server Settings

   Set up the LDAP server connection.

Make sure the rest of the settings looks similar to :numref:`piwik-ldap`. Note that ``Required User Group`` should be
set to ``cn=piwik,ou=groups,dc=example,dc=com``, where ``dc=example,dc=com`` should be replaced by the ``$LDAP_SUFFIX``
in :doc:`../install-essential-docker/openldap`. Click on the ``Test`` link in the ``Required User Group`` box to make
sure the configuration is correct. Then click ``Save``.

The configuration above is the recommended settings, but we can also follow `LoginLdap configuration guide
<https://github.com/piwik/plugin-LoginLdap#configurations>`_ to configure the plugin differently.

Update Piwik
------------

The Piwik container used here is a self-managed php container, which means that all Piwik files are downloaded and
stored in a data container during the Piwik container's first run. To upgrade, simply use Piwik's builtin auto updater.

To manually update, run the following command to enter the shell in the Piwik container then switch to ``/var/www``:
::

   ne piwik
   # Now in the Piwik container
   cd /var/www

Then follow the `manual update instructions <https://piwik.org/docs/update/>`_ to update.

.. _Piwik: https://piwik.org
