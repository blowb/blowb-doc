Install Internet Apps in Docker Containers
==========================================

.. index:: Internet app

In this chapter, we will install Internet apps (Internet service software) with which users directly interact, such as
file/contact/calendar syncing (ownCloud), Web Analytics (Piwik), instant messaging (XMPP), etc. None of these software
is essential in this framework, so you can choose to install only the ones which you need.

.. index:: Nginx, dnsmasq, MariaDB, OpenLDAP, Postfix
   single: Docker; data container

.. rubric:: Basic Rules

This chapter only introduces a limited number of Internet apps, to serve as examples. In this chapter, all of the
Internet apps are configured to be fit in the framework introduced in :doc:`../overview`. The basic rules for deploying
an Internet app are (as illustrated in :numref:`overview-diagram`):

- If needed, forward Nginx incoming connections to the Internet app.
- If needed, use the dnsmasq instance on the host to look up other services (containers).
- If needed, use the MariaDB instance configured in :doc:`../install-essential-docker/mariadb` as the SQL database.
- If needed, use the OpenLDAP instance configured in :doc:`../install-essential-docker/openldap` for authentication.
- If needed, use the Postfix instance configured in :doc:`../setup-host/postfix` for sending out emails.
- If needed, add a data container for data storage on the file system.

As long as an Internet app can be deployed complying the rules above, it would fit in this framework.

At the beginning of each section in this chapter, the rules above followed by the corresponding Internet app deployment
are listed for easier reference.

.. index:: MariaDB, Docker
   single: Internet app; upgrade

.. rubric:: Upgrade an Internet App

Unless otherwise stated, to upgrade an Internet app, follow the following steps:

1. pull the latest image: ``docker pull the-image``,

2. remove the currently running container by executing ``docker rm -f container``,

3. run the same ``docker run`` command as same as the first time the container was started,

4. run ``flush hosts`` in the MariaDB shell if MariaDB is used for this app to empty the MariaDB host cache (similar to
   :doc:`../common-tasks/add-mariadb-database`, but only run ``flush hosts`` after entering the MariaDB shell).

.. toctree::
   :caption: Table of Contents
   :name: install_service_toc
   :maxdepth: 2

   owncloud
   piwik
   prosody
   isso
   ltb-self-service-password
   mozilla-sync
