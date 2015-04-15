Create a New Database and User in MariaDB
=========================================

This section describes how to create a new database and a new user in MariaDB.

Before we operate on MariaDB, we need to generate a password for this new MariaDB user. you can run ``cat /dev/urandom
| tr -dc 'a-zA-Z0-9' | fold -w N | head -1``, where ``N`` is the length of the password. A password with a length of at
least 10 is recommended.

Then we need to enter the MariaDB container shell:
::

   ne mariadb

Inside the shell of the MariaDB container, run the following command to start MariaDB shell:
::

   mysql -u root -p

After enter the root password of your MariaDB instance, you should now be in the MariaDB shell. After replacing
``newuser`` with the new user's user name, ``newdb`` with the new database name you want to create, and ``PASSWORD``
with the password your generated earlier in this section, run the following SQL commands:

.. code-block:: sql

   CREATE USER 'newuser' IDENTIFIED BY 'PASSWORD';
   CREATE DATABASE newdb;
   GRANT ALL PRIVILEGES ON newdb.* TO 'newuser';
   FLUSH PRIVILEGES;

The SQL statements above creates a new user ``newuser`` with a password of ``PASSWORD`` and a new database ``newdb``,
and grants ``newuser`` the privilege to perform all operations on the database ``newdb``.

Press ``Ctrl-D`` twice to exit the MariaDB shell and the container's shell.