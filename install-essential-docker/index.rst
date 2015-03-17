Install Essential Software in Docker Containers
===============================================

In this chapter we'll install some essential software in Docker containers. Before we proceed,
create a directory used to share files between the host and the containers:
::

   sudo mkdir /var/docker

If you have SELinux enabled, you should also run:
::

   sudo chcon -t svirt_sandbox_file_t /var/docker

Contents:

.. toctree::
   :maxdepth: 2

   install-nginx
   install-mariadb
