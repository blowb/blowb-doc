..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Install Essential Software in Docker Containers
===============================================

In this chapter we'll install some essential software in Docker containers. Before we proceed,
create a directory used to share files between the host and the containers:
::

   export DOCKER_SHARE=/var/docker
   echo 'export DOCKER_SHARE=/var/docker' >> ~/.bashrc
   sudo mkdir $DOCKER_SHARE

If you have SELinux enabled, you should also run:
::

   sudo chcon -t svirt_sandbox_file_t $DOCKER_SHARE

.. toctree::
   :caption: Table of Contents
   :maxdepth: 2

   nginx
   mariadb
   openldap
