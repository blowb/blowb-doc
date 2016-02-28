LTB Self Service Password, Allowing Users to Change Their Passwords
===================================================================

.. index:: OpenLDAP, Postfix, Nginx, dnsmasq
   single: LTB; Self Service Password

*This Internet app uses dnsmasq, Nginx, OpenLDAP and Postfix.*

`LTB Self Service Password`_ is a PHP application which allows users to change their passwords in the LDAP database. It
is part of the `LTB`_ project (LDAP Tool Box Project), which aims at easing LDAP administration.

Configure DNS
-------------

Add an ``A`` record to point the domain you want to use with LTB Self Service Password to the IP address of the
server.

Start the LTB Self Service Password Container
---------------------------------------------

First pull the LTB Self Service Password Docker image:
::

   docker pull blowb/ltb-self-service-password

Create a directory to store LTB Self Service Password configuration files:
::

   sudo mkdir $DOCKER_SHARE/ltb-self-service-password

Generate the default configuration file:
::

   cd $DOCKER_SHARE/ltb-self-service-password
   sudo -s <<< "docker run --rm blowb/ltb-self-service-password \
    cat /var/www/ltb-self-service-password/conf/config.inc.php > config.inc.php"

Run the following commands to modify the configuration file, after replacing ``dc=example,dc=com`` with the
``$LDAP_SUFFIX`` in :doc:`../install-essential-docker/openldap`, ``password@example.com`` with the notification
email you want to use, and ``MY_LDAP_ROOT_PASSWORD`` with the root password of the OpenLDAP server:

.. code-block:: bash
   :linenos:

   LDAP_SUFFIX='dc=example,dc=com'
   NOTIFICATION_FROM=password@example.com
   sudo ed config.inc.php << EOF
   %s/^\(\$ldap_url =\).*/\1 "ldap:\/\/ldap";
   %s/^\(\$ldap_binddn =\).*/\1 "cn=root,$LDAP_SUFFIX";
   %s/^\(\$ldap_bindpw =\).*/\1 "MY_LDAP_ROOT_PASSWORD";
   %s/^\(\$ldap_base =\).*/\1 "ou=people,$LDAP_SUFFIX";
   %s/^\(\$who_change_password =\).*/\1 "manager";
   %s/^\(\$mail_from =\).*/\1 "$NOTIFICATION_FROM";
   wq
   EOF

Explanation:

  - **line 4**: the LDAP server URL will be named ``ldap``;
  - **line 5**: set the root DN;
  - **line 6**: set the root password of the OpenLDAP server;
  - **line 7**: set the search base;
  - **line 8**: let the root user change password not the user itself;
  - **line 9**: the "from" email address of the notification mails.

Optionally we can further modify the configuration file ``config.inc.php`` to adjust settings:
::

   sudo $EDITOR config.inc.php

Start the container:
::

   docker run --restart always -d --name ltb-self-service-password \
    --dns $HOST_ADDR --add-host smtp-server:$HOST_ADDR -v \
    $DOCKER_SHARE/ltb-self-service-password/config.inc.php:/etc/config.inc.php:ro \
    blowb/ltb-self-service-password

The Dockerfile from which the image was generated is `available
<https://hub.docker.com/r/blowb/ltb-self-service-password/~/dockerfile/>`_.

Configure Nginx
---------------

After replacing ``password.example.com`` with the domain to be used for accessing the password reset page, run the
following command:
::

   echo --volumes-from ltb-self-service-password >> ~/util/nginx-volumes.txt
   cd $DOCKER_SHARE/nginx
   LTB_SSP_URL='password.example.com'
   sudo -s <<EOF
   sed -e "s/@server_name@/$LTB_SSP_URL/g" \
   redirect-https.conf.tmpl > ltb-self-service-password.conf
   sed -e "s/@server_name@/$LTB_SSP_URL/g" \
   -e 's/@root@/ltb-self-service-password/g' \
   -e 's/@fastcgi_server@/ltb-self-service-password:9000/g' \
   fastcgi.tls.conf.tmpl > ltb-self-service-password.tls.conf
   EOF

You can edit ``ltb-self-service-password.tls.conf`` to use your own tls/ssl key if you don't want to use the dummy key.

Recreate and restart the Nginx container:
::

   ~/util/rerun-nginx.sh

.. _LTB: http://ltb-project.org
.. _LTB Self Service Password: http://ltb-project.org/wiki/documentation/self-service-password
