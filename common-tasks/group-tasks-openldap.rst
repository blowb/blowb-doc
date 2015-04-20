Common Group Related Tasks in the OpenLDAP Database
===================================================

In this section, we will add a group named ``newgroup`` under ``ou=groups,dc=example,dc=com`` in the OpenLDAP
database, where ``dc=example,dc=com`` corresponds to your domain. We will also show how to add a user to an existing
group.

Enter the OpenLDAP container:
::

   ne openldap

In the OpenLDAP container, run the following command to set up domain and the new group name as bash variables (replace
``example.com`` with your domain configured in :doc:`Install and Configure OpenLDAP`):
::

   MY_DOMAIN=example.com
   LDAP_SUFFIX=$(sed -e 's/^/dc=/' -e 's/\./,dc=/g' <<< $MY_DOMAIN)
   NEWGROUP=newgroup

Add a New Group into the OpenLDAP Database
------------------------------------------

Run the following command to create the new group ``newgroup`` (replace ``MY_PASSWORD`` with your OpenLDAP root
password, ``uid`` with a user name you want to add to the group):
::

   ldapadd -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: cn=$NEWGROUP,ou=groups,$LDAP_SUFFIX
   cn: $NEWGROUP
   objectclass: groupOfNames
   member: cn=uid,$LDAP_SUFFIX
   EOF

Remember that the ``member:`` line is necessary, and it can appear multiple times to add more than one person to the
group.

Add a Member to an Existing Group
---------------------------------

Run the following command to add the user ``uid`` to the group ``newgroup`` (replace ``MY_PASSWORD`` with your OpenLDAP
root password):
::

   ldapmodify -H ldapi:/// -x -w MY_PASSWORD -D "cn=root,$LDAP_SUFFIX" <<EOF
   dn: cn=$NEWGROUP,ou=groups,$LDAP_SUFFIX
   changetype: modify
   add: member
   member: cn=uid,ou=people,$LDAP_SUFFIX
   EOF
