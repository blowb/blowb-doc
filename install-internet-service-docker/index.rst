Install Internet Service Software in Docker Containers
======================================================

In this chapter, we will install Internet service software with which users directly interact, such as
file/contact/calendar syncing (ownCloud), information publishing (Wordpress), instant messaging (XMPP), etc. None of
these software is essential, which means that you can choose to install only the ones which you need.

In this chapter, you will need to set up a MariaDB database password for each service which uses MariaDB. To generate a
password, you can run ``cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w N | head -1``, where ``N`` is the length of the
password. I suggest to use a password with length greater than 10.

.. toctree::
   :caption: Table of Contents
   :maxdepth: 2

   isso
   mozilla-sync
   piwik
   prosody
