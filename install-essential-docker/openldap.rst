Install OpenLDAP
================

.. index:: OpenLDAP
   see: slapd; OpenLDAP

Start the OpenLDAP Container
----------------------------

We will use ``slapd`` (part of `OpenLDAP`_) as the main database to manage users including authentication. Using an LDAP
server makes it much easier to manage users, such as adding a new user, deleting a user, and modifying a user's
password.

Create a data container to store OpenLDAP data and config:
::

   docker run -v /var/lib/ldap -v /etc/openldap/slapd.d --name openldap-data \
    busybox /bin/true

- If you have an old database to import, you can copy them into the data container now (configuration into
  :file:`/etc/openldap/slapd.d`, and data into :file:`/var/lib/ldap`).

- If this is a new database, run the command below to fill the configuration directory (:file:`/etc/openldap/slapd.d`)
  with default configuration:
  ::

     docker run --rm --volumes-from openldap-data centos:7 \
      yum install -y openldap-servers

Now we can create and run the ``openldap`` container:
::

   docker run --restart always -d --volumes-from openldap-data \
    --env MAX_NOFILE=8192 --name openldap blowb/openldap

``MAX_NOFILE`` is the maximal number of files that the ``slapd`` process can open. The larger this file is, the more RAM
this process would need. A number such as 8192 should be enough for a small database.

If you have imported an old database and configuration, you may want to check some potential compatibility issues and
skip to `Manage the LDAP Database with a GUI frontend`_. If this is a new OpenLDAP database, we have a little more work
to do.

Configure OpenLDAP
------------------

.. index:: LDAP_SUFFIX, root DN

First, we need to change the database suffix and the root DN. Run ``ne openldap`` to launch the shell inside the
OpenLDAP container. Inside the container, run the following command, after replacing ``example.com`` with the domain we
want to use:
::

   MY_DOMAIN=example.com
   LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)
   ldapmodify -H ldapi:/// <<EOF
   dn: olcDatabase={2}hdb,cn=config
   changetype: modify
   replace: olcSuffix
   olcSuffix: $LDAP_SUFFIX

   dn: olcDatabase={2}hdb,cn=config
   changetype: modify
   replace: olcRootDN
   olcRootDN: cn=root,$LDAP_SUFFIX

   EOF

If you see messages similar to the following lines, then the modification should be successful:

.. code-block:: none

   modifying entry "olcDatabase={2}hdb,cn=config"

   modifying entry "olcDatabase={2}hdb,cn=config"

Next we are going to set up a password for the root DN. First, generate the hash of the password (follow the prompt to
enter password):
::

   HASHED_PASSWD=$(slappasswd)

Then, update the password in the configuration file:
::

   ldapmodify -H ldapi:/// <<EOF
   dn: olcDatabase={2}hdb,cn=config
   changetype: modify
   add: olcRootPW
   olcRootPW: $HASHED_PASSWD
   EOF

Add some basic schemata:
::

   ldapadd -H ldapi:/// -f /etc/openldap/schema/core.ldif
   ldapadd -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
   ldapadd -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif

Add the domain (replace ``MY_PASSWORD`` with the actual password):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: $LDAP_SUFFIX
   objectClass: domain
   dc: $(sed -e 's/,.*//' -e 's/dc=//' <<< $LDAP_SUFFIX)
   EOF

Add an organization unit to store the user data (replace ``MY_PASSWORD`` with the actual password):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: ou=people,$LDAP_SUFFIX
   ou: people
   description: All users.
   objectClass: organizationalUnit
   EOF

Next, we will add a minimal user entry for ourselves (and other users if they do not oppose to type their password here
in the terminal). First run ``slappasswd`` to generate the hashed password:
::

   HASHED_PASSWD=$(slappasswd)

Then run the following commands, after replacing ``username`` with the user name, ``fullname`` with the full name,
``surname`` with the surname (sure, both ``fullname`` and ``surname`` can be faked), and ``me@example.com`` with the
email of the new account:
::

   UN='username' CN='fullname' SN='surname' MAIL='me@example.com'
   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: uid=$UN,ou=people,$LDAP_SUFFIX
   uid: $UN
   objectClass: inetOrgPerson
   cn: $CN
   sn: $SN
   mail: $MAIL
   userPassword: $HASHED_PASSWD
   EOF

.. index::
   single: OpenLDAP; group

We also need to add a group branch to control users' accessibility to Internet apps (replace ``MY_PASSWORD`` with the
actual password):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: ou=groups,$LDAP_SUFFIX
   ou: groups
   description: All groups.
   objectClass: organizationalUnit
   EOF

We also need to set up the ``memberOf`` overlay so that we queries can use ``memberOf``:
::

   ldapadd -H ldapi:/// <<EOF
   dn: cn=module,cn=config
   cn: module
   objectclass: olcModuleList
   objectclass: top
   olcmoduleload: memberof.la
   olcmodulepath: /usr/lib64/openldap

   dn: olcOverlay={0}memberof,olcDatabase={2}hdb,cn=config
   objectClass: olcConfig
   objectClass: olcMemberOf
   objectClass: olcOverlayConfig
   objectClass: top
   olcOverlay: memberof

   dn: cn=module,cn=config
   cn: module
   objectclass: olcModuleList
   objectclass: top
   olcmoduleload: refint.la
   olcmodulepath: /usr/lib64/openldap

   dn: olcOverlay={1}refint,olcDatabase={2}hdb,cn=config
   objectClass: olcConfig
   objectClass: olcOverlayConfig
   objectClass: olcRefintConfig
   objectClass: top
   olcOverlay: {1}refint
   olcRefintAttribute: memberof member manager owner

   EOF

Press ``Ctrl+D`` to exit the container shell.

.. index:: dnsmasq

Finally, add a DNS record to specify ``ldap`` as an alias of ``openldap`` and restart ``dnsmasq``:
::

   sudo -s <<< "echo 'cname=ldap,openldap' > /etc/dnsmasq.d/ldap"
   sudo systemctl restart dnsmasq

.. index::
   single: OpenLDAP; GUI
   JXplorer

Manage the LDAP Database with a GUI frontend
--------------------------------------------

To make managing the LDAP database easier, we probably want to use a GUI frontend, such as `JXplorer`_. In order to
connect to the slapd process, we need the container's IP address and port number. Use the following command to display
the IP address of the OpenLDAP container:
::

   docker inspect --format '{{.NetworkSettings.IPAddress}}' openldap

The default port number is 389.

.. index:: SSH tunneling, VNC

If the server is physically accessible and it has a desktop environment installed (such as GNOME, KDE), we can install a
GUI front end and connect to the ``slapd`` process through TCP/IP. If the server is managed remotely, we can either (a)
use a VNC server, or (b) use SSH tunneling. Here we will use the SSH tunneling method.

First, install a GUI LDAP frontend locally on the client side. Then, assuming the client system is a POSIX-compliant
system (GNU/Linux, FreeBSD, Mac OS X, etc), use the following command to build an SSH tunnel:
::

   ssh -L 12345:slapd_ip:389 username@server.tld

.. index:: plink

where ``slapd_ip`` is the IP address of the OpenLDAP container, ``server.tld`` is the server's address, and ``username``
is the user name of the POSIX account on the server (Windows users may replace ``ssh`` with `plink`_). By launching the
GUI front end and connect to ``localhost:12345``, we should be able to connect to the OpenLDAP server that we have just
set up.

.. _`JXplorer`: http://jxplorer.org/
.. _`OpenLDAP`: http://www.openldap.org/
.. _`plink`: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
