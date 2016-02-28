Install Essential Software in Docker Containers
===============================================

.. index:: DOCKER_SHARE

In this chapter we will install some essential software in Docker containers. Before we proceed,
create a directory used to share files between the host and the containers:
::

   export DOCKER_SHARE=/var/docker
   echo 'export DOCKER_SHARE=/var/docker' >> ~/.bashrc
   sudo mkdir $DOCKER_SHARE

.. index:: SELinux

If SELinux is enabled, also run the following command:
::

   sudo chcon -t svirt_sandbox_file_t $DOCKER_SHARE

.. toctree::
   :caption: Table of Contents
   :name: essential_docker_toc
   :maxdepth: 2

   nginx
   mariadb
   openldap
