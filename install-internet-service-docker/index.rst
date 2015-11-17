Install Internet Service Software in Docker Containers
======================================================

In this chapter, we will install Internet service software with which users directly interact, such as
file/contact/calendar syncing (ownCloud), information publishing (Wordpress), instant messaging (XMPP), etc. None of
these software is essential, so you can choose to install only the ones which you need.

.. rubric:: Basic Rules

This chapter only introduces a limited number of Internet service software, to serve as examples. In this chapter, all
of the Internet apps are configured to be fit in the framework introduced in :doc:`../overview`. The basic rules for
each Internet app are (as illustrated in :numref:`overview-diagram`):

- If needed, forward Nginx incoming connections to the Internet app.
- If needed, use the dnsmasq instance on the host to look up other services.
- If needed, use the MariaDB instance configured in :doc:`../install-essential-docker/mariadb` for database.
- If needed, use the OpenLDAP instance configured in :doc:`../install-essential-docker/openldap` for authentication.
- If needed, use the Postfix instance configured in :doc:`../setup-host/postfix` for sending out emails.
- If needed, add a data container for data storage on the filesystem.

As long as you can configure an app following the rules above, your app would fit in this framework.

At the beginning of each section in this chapter, the rules above followed for the corresponding app are listed and thus
easier for you to look up.

.. rubric:: Upgrade an Internet App

Unless otherwise stated, to upgrade a specific app, you need to:

1. pull the latest image: ``docker pull the-image``,
2. remove the container by running ``docker rm -f container``,
3. run the same ``docker run`` command as the same as the first time the container was started,
4. run ``flush hosts`` in the MariaDB shell if MariaDB is used for this app (similar to
   :doc:`../common-tasks/add-mariadb-database`, but only run ``flush hosts`` after entering the MariaDB shell).

.. toctree::
   :caption: Table of Contents
   :name: install_service_toc
   :maxdepth: 2

   isso
   ltb-self-service-password
   mozilla-sync
   owncloud
   piwik
   prosody
