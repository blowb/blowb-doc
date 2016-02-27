Create a New Database and User in MariaDB
=========================================

This section describes the procedure to create a new database and a new user in MariaDB.

Before we operate on MariaDB, we need to generate a password for this new MariaDB user. To generate a random password,
we can run ``cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w N | head -1``, where ``N`` is the length of the password. A
password with a length of at least 10 is recommended.

Then we need to enter the MariaDB container shell:
::

   ne mariadb

Inside the shell of the MariaDB container, run the following command to start MariaDB shell:
::

   mysql -u root -p

After entering the MariaDB root password, we should now be in the MariaDB shell. Run the following SQL commands, after
replacing ``newuser`` with the new user's user name, ``userhost`` with the host from which the user connects (if you
followed :doc:`../setup-host/dnsmasq`, this should be simply the name of the container of the Internet app), ``newdb``
with the name of the new database to be created, and ``PASSWORD`` with the password generated earlier in this section:

.. code-block:: mysql

   CREATE USER 'newuser'@'userhost' IDENTIFIED BY 'PASSWORD';
   CREATE DATABASE newdb;
   GRANT ALL PRIVILEGES ON newdb.* TO 'newuser'@'userhost';
   FLUSH PRIVILEGES;

The SQL commands above creates a new user ``newuser`` with a password of ``PASSWORD`` and a new database ``newdb``,
and grants ``newuser`` the privilege to perform all operations on the database ``newdb``.

Press ``Ctrl-D`` twice to exit the MariaDB shell and the container shell.
