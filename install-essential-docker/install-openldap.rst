Install OpenLDAP
================

We will use slapd (part of `OpenLDAP`_) as the main authentication service. Using an LDAP server to manage users makes it
much easier to make changes to users', such as adding a new user, deleting a user, or modifying users' password.

Create a data container to store OpenLDAP data and config:
::

   docker run -v /var/lib/ldap -v /etc/openldap/slapd.d --name openldap-data busybox /bin/true

- If you have an old database to import, you can copy them into the data container now (configuration into
  :file:`/etc/openldap/slapd.d`, and data into :file:`/var/lib/ldap`).

- If you are creating a new database, run the command below to fill the configuration directory
  (:file:`/etc/openldap/slapd.d`) with default configuration:
  ::

     docker run --rm --volumes-from openldap-data centos:7 yum install -y openldap-servers

Now we can create and run the ``openldap`` container:
::

   docker run --restart always -d --volumes-from openldap-data --env MAX_NOFILE=8192 --name openldap blowb/openldap

``MAX_NOFILE`` is the maximal number of files that the slapd process can open. The larger this file is, the more RAM
this process would need. Lower the number to 8192 should be enough for a small database.

If you've imported an old database and configuration, you may want to check some compatibility issues you may have and
skip the rest of this section. If this is your new OpenLDAP database, we have a little more work to do.

We need to change the database suffix and the root DN. Run ``ne openldap`` to launch the shell inside the OpenLDAP
container. Inside the container, run the following command, after replacing ``example.com`` with your domain:
::

   MY_DOMAIN=example.com
   LDAP_DOMAIN=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)
   ldapmodify -H ldapi:/// <<EOF
   dn: olcDatabase={2}hdb,cn=config
   changetype: modify
   replace: olcSuffix
   olcSuffix: $LDAP_DOMAIN

   dn: olcDatabase={2}hdb,cn=config
   changetype: modify
   replace: olcRootDN
   olcRootDN: cn=users,$LDAP_DOMAIN

   EOF

If you see messages similar to the following line, then the modification should be successful:

.. code-block:: none
   modifying entry "olcDatabase={2}hdb,cn=config"

   modifying entry "olcDatabase={2}hdb,cn=config"

Press ``Ctrl+D`` to exit the container shell.




.. _`OpenLDAP`: http://www.openldap.org/
