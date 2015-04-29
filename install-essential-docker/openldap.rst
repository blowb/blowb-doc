..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Install and Configure OpenLDAP
==============================

Start the OpenLDAP Container
----------------------------

We will use ``slapd`` (part of `OpenLDAP`_) as the main authentication service. Using an LDAP server to manage users
makes it much easier to make changes to users', such as adding a new user, deleting a user, or modifying users'
password.

Create a data container to store OpenLDAP data and config:
::

   docker run -v /var/lib/ldap -v /etc/openldap/slapd.d --name openldap-data \
    busybox /bin/true

- If you have an old database to import, you can copy them into the data container now (configuration into
  :file:`/etc/openldap/slapd.d`, and data into :file:`/var/lib/ldap`).

- If you are creating a new database, run the command below to fill the configuration directory
  (:file:`/etc/openldap/slapd.d`) with default configuration:
  ::

     docker run --rm --volumes-from openldap-data centos:7 \
      yum install -y openldap-servers

Now we can create and run the ``openldap`` container:
::

   docker run --restart always -d --volumes-from openldap-data \
    --env MAX_NOFILE=8192 --name openldap blowb/openldap

``MAX_NOFILE`` is the maximal number of files that the ``slapd`` process can open. The larger this file is, the more RAM
this process would need. Lower the number to 8192 should be enough for a small database.

If you've imported an old database and configuration, you may want to check some compatibility issues you may have and
skip to `Manage the LDAP Database with a GUI frontend`_. If this is your new OpenLDAP database, we have a little more
work to do.

Configure OpenLDAP
------------------

First, we need to change the database suffix and the root DN. Run ``ne openldap`` to launch the shell inside the
OpenLDAP container. Inside the container, run the following command, after replacing ``example.com`` with your domain:
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

Add some basic schema:
::

   ldapadd -H ldapi:/// -f /etc/openldap/schema/core.ldif
   ldapadd -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
   ldapadd -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif

Add the domain (replace ``MY_PASSWORD`` with your actual password):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: $LDAP_SUFFIX
   objectClass: domain
   dc: $(sed -e 's/,.*//' -e 's/dc=//' <<< $LDAP_SUFFIX)
   EOF

Add an organization unit to store the user data (replace ``MY_PASSWORD`` with your actual password):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: ou=people,$LDAP_SUFFIX
   ou: people
   description: All users.
   objectClass: organizationalUnit
   EOF

Next, add minimal user entries for yourself (and other users if they do not oppose to type their password here in the
terminal). First run ``slappasswd`` to generate the hashed password:
::

   HASHED_PASSWD=$(slappasswd)

Then run the following command, after replacing ``username`` with the user name of the new account, ``fullname`` with
the full name of the user, ``surname`` with the surname of your new account (sure, both ``fullname`` and ``surname`` can
be faked), and ``me@example.com`` with the email of the new account:
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

We also need to add a group branch to control users' accessibility to services (replace ``MY_PASSWORD`` with your actual
password):
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

Finally, add a DNS record to alias ``db`` to ``mariadb`` and restart ``dnsmasq``:
::

   sudo -s <<< "echo 'cname=ldap,openldap' > /etc/dnsmasq.d/ldap"
   sudo systemctl restart dnsmasq

Manage the LDAP Database with a GUI frontend
--------------------------------------------

To make managing the LDAP database easier, you probably want to use a GUI frontend, such as `JXplorer`_. You need the
container's IP address and port number to connect to the slapd process. Use the following command to display the IP
address of the OpenLDAP container:
::

   docker inspect --format '{{.NetworkSettings.IPAddress}}' openldap

The default port number is 389.

If you can access your server physically and you have a desktop environment installed on your server (such as GNOME),
you can install a GUI front end, and connect to the ``slapd`` process through TCP/IP. If you are managing the server
remotely, you can either (a) use a VNC server, or (b) use SSH tunneling. Here I will introduce the SSH tunneling method.

First, install a GUI LDAP frontend locally. Then, assuming you are managing the server on a POSIX compliant system
(GNU/Linux, FreeBSD, Mac OS X, etc), use the following command to build a SSH tunnel:
::

   ssh -L 12345:slapd_ip:389 username@yourserver.tld

where ``slapd_ip`` is the IP address of the OpenLDAP container, ``yourserver.tld`` is your server's address,
``username`` is the user name of your account on the server (Windows users may replace ``ssh`` with `plink`_).  Launch
your GUI frontend and connect to ``localhost:12345``, then you should be able to connect to the OpenLDAP server you've
just set up.

.. _`JXplorer`: http://jxplorer.org/
.. _`OpenLDAP`: http://www.openldap.org/
.. _`plink`: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
