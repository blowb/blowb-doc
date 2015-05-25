..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Install Internet Service Software in Docker Containers
======================================================

In this chapter, we will install Internet service software with which users directly interact, such as
file/contact/calendar syncing (ownCloud), information publishing (Wordpress), instant messaging (XMPP), etc. None of
these software is essential, so you can choose to install only the ones which you need.

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
