Install MariaDB
===============

We will use `MariaDB`_ as the main database.

Run the following command to create a data container:
::

   docker run -v /var/lib/mysql --name dbdata busybox /bin/true

The default MariaDB configuration is sometimes too large for your server, thus we can try to download a configuration
file which is suitable for the server. There are official templates for 5 different sizes of hardware resource:
``small``, ``medium``, ``large``, ``huge``, ``innodb-heavy-4G``. The criteria to choose any of them are written in the
comments of these template configuration files. For convenience, I pasted the relevant part below:

  - **small**: This is for a system with little memory (<= 64M) where MariaDB is only used from time to time and it's
    important that the mysqld daemon doesn't use much resources.

  - **medium**: This is for a system with little memory (32M - 64M) where MariaDB plays an important part, or systems up
    to 128M where MariaDB is used together with other programs (such as a web server).

  - **large**: This is for a large system with memory = 512M where the system runs mainly MariaDB.

  - **huge**: This is for a large system with memory of 1G-2G where the system runs mainly MariaDB.

  - **innodb-heavy-4G**: This is for systems with 4GB of memory running mostly MariaDB using InnoDB only tables and
    performing complex queries with few connections.

Very likely **small** isn't enough for our use case, as the Internet service software we will install probably uses
MariaDB as an important part. You can start with **medium** if you are not sure how much resource your MairaDB instance
would use.

Run the following commands to download and do some preprocessing of your MariaDB configuration files, where
``YOUR_SIZE`` should be replaced with one of ``small``, ``medium``, ``large``, ``huge`` or ``innodb-heavy-4G``:

.. code-block:: bash
   :linenos:

   export SIZE=YOUR_SIZE
   sudo mkdir $DOCKER_SHARE/mariadb
   sudo -E wget -O $DOCKER_SHARE/mariadb/my.cnf \
    https://github.com/MariaDB/server/raw/10.0/support-files/my-$SIZE.cnf.sh
   sudo sed -ri -e 's/^(bind-address|skip-networking|socket)/#\1/' \
    -e 's/@MYSQL_TCP_PORT@/3306/' \
    -e 's/^#(innodb_buffer_pool_size|innodb_log_file_size|innodb_log_buffer_size)/\1/' \
    -e '/^\[mysqld\]/a \
   user\t\t= mysql\
   character-set-server = utf8 \
   collation-server = utf8_general_ci' \
    -e '/^\[client\]/a \
   default-character-set = utf8' $DOCKER_SHARE/mariadb/my.cnf
   sudo -s <<EOF
   echo >> $DOCKER_SHARE/mariadb/my.cnf
   echo '!includedir /etc/mysql/conf.d/' >> $DOCKER_SHARE/mariadb/my.cnf
   EOF
   unset SIZE

Explanation:

  - **line 5:** don't set ``bind-address``, ``skip-networking``, or ``socket``;

  - **line 6:** use 3306 as the MariaDB listening port;

  - **line 7:** enable some innodb relevant options;

  - **line 8-13:** run MariaDB as user "mysql" and use UTF-8 encoding.

Optionally you can also adjust other parameters in the config file at this point:
::

   sudo $EDITOR $DOCKER_SHARE/mariadb/my.cnf

Start the MariaDB container with the following command, after replacing ``'PASSWORD'`` with your own password:
::

   docker run --restart always -d --volumes-from dbdata \
    -v $DOCKER_SHARE/mariadb/my.cnf:/etc/mysql/my.cnf:ro \
    -e MYSQL_ROOT_PASSWORD='PASSWORD' --dns $HOST_ADDR \
    --name mariadb mariadb:10.0

Since our command line history has recorded the root password of MariaDB, we need to clear the
relevant history entries:
::

   history -a
   sed -i '/MYSQL_ROOT_PASSWORD/d' ~/.bash_history

The commands above first write all histories in RAM to the history file, then delete all history
entries which contains ``MYSQL_ROOT_PASSWORD``.

We then need to disable remote root access of the MariaDB instance for better security. enter the MariaDB container
shell:
::

   ne mariadb

Inside the shell of the MariaDB container, run the following command to start MariaDB shell:
::

   mysql -u root -p

Execute the following SQL statement:

.. code-block:: mysql

   rename user 'root'@'%' to 'root'@'localhost';

The SQL statement above limits root access to localhost only.

Press ``Ctrl-D`` twice to exit the MariaDB shell and the container's shell.

Finally, add a DNS record to alias ``db`` to ``mariadb`` and restart ``dnsmasq``:
::

   sudo -s <<< "echo 'cname=db,mariadb' > /etc/dnsmasq.d/db"
   sudo systemctl restart dnsmasq

.. _MariaDB: https://mariadb.org
