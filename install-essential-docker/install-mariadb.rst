Install MariaDB
===============

We will use `MariaDB`_ as the main database.

Run the following command to create a data container:
::

   docker create -v /var/lib/mysql --name dbdata scratch /bin/true

Start the MariaDB container with the following command, after replacing ``'PASSWORD'`` with your own
password:
::

   docker run --restart always -d --volumes-from dbdata \
    -e MYSQL_ROOT_PASSWORD='PASSWORD' --name mariadb mariadb:10.0

Since our command line history has recorded the root password of MariaDB, we need to clear the
relevant history entries:
::

   history -a
   sed -i '/MYSQL_ROOT_PASSWORD/d' ~/.bash_history

The commands above first write all histories in RAM to the history file, then delete all history
entries which contains ``MYSQL_ROOT_PASSWORD``.

.. _MariaDB: http://www.mariadb.org
