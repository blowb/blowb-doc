Install Docker
==============

`Docker`_ is an essential software in Blowb. Most of our services will be installed into a docker
container for better isolation.

Run the following command to install Docker (you need to enable the ``extra`` repo if you are on Red Hat Enterprise
Linux):
::

   sudo yum install docker

Set up Docker Storage Options
-----------------------------

By default, Docker storage uses devicemapper storage driver in the loopback mode. However, this default setting is
strongly discouraged for production use. Here, the overlay storage driver will be used, but you are free to explore
`other storage options <https://docs.docker.com/engine/userguide/storagedriver/selectadriver/>`__. If you have your own
idea of storage options, you can skip to the section `Enable and Start Docker`_.

To change the storage options, set the ``DOCKER_STORAGE_OPTIONS`` in ``/etc/sysconfig/docker-storage``:
::

   sudo sed -i '/DOCKER_STORAGE_OPTIONS=/s/$/-s overlay/' /etc/sysconfig/docker-storage

Since SELinux is not supported by the ``overlay`` driver, the SELinux support for Docker should be disabled by removing
``--selinux-enabled`` from the Docker options in ``/etc/sysconfig/docker``:
::

   sudo sed -i '/OPTIONS=/s/--selinux-enabled//' /etc/sysconfig/docker

On some Red Hat systems, a service ``docker-storage-setup`` is available on the system (you can check this by executing
``systemctl | grep docker-storage-setup``). In this case, you need to disable it:
::

   sudo systemctl disable docker-storage-setup

.. _enable-start-docker:

Enable and Start Docker
-----------------------

Now you can start Docker and make Docker start at boot:
::

   sudo systemctl enable docker
   sudo systemctl start docker

Miscellaneous Setup for Convenient Administration
-------------------------------------------------

To use docker as a non-root user:
::

    sudo groupadd docker
    sudo usermod -a -G docker $USER

It will let you run docker without root access. Remember you need to relogin to make the group
change take effect.

Since you may need to use `nsenter`_ to enter the container, for convenience, run the command below to add a function to
enter a container easily:
::

   cat >>~/.bashrc << 'EOF'
   ne () {
     pid=$(docker inspect --format '{{.State.Pid}}' $1)
     env SHELL='/bin/bash' sudo -E nsenter --target $pid \
      --mount --uts --ipc --net --pid
   }
   EOF

Also run the following command:
::

   ifconfig docker0

The output should be similar to the following:

.. code-block:: none

    docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 172.17.42.1  netmask 255.255.0.0  broadcast 0.0.0.0
            inet6 fe80::5484:7aff:fefe:9799  prefixlen 64  scopeid 0x20<link>
            ether 56:84:7a:fe:97:99  txqueuelen 0  (Ethernet)
            RX packets 39  bytes 1828 (1.7 KiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 45  bytes 4050 (3.9 KiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

You may have a different IP address after ``inet``. Export the ``inet`` entry to a variable, which
will be used later. In this example it should be:
::

   echo 'export HOST_ADDR=172.17.42.1' >> ~/.bashrc

Remember to replace ``172.17.42.1`` with the output on your system!

Reload ``~/.bashrc``:
::

   source ~/.bashrc

.. _Docker: https://www.docker.com
.. _nsenter: http://blog.docker.com/tag/nsenter/
