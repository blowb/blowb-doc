Install Docker
==============

`Docker`_ is an essential software in Blowb. Most of our services will be installed into a docker
container for better isolation.

Run the following command to install docker:
::

   sudo yum install docker

Start docker and make docker start at boot:
::

   sudo systemctl start docker
   sudo systemctl enable docker

To use docker as a non-root user:
::

    sudo usermod -a -G docker $USER

It will let you run docker without root access. Remember you need to relogin to make the group
change take effect.

Since we may need to use `nsenter`_ to enter the container, for convenience, run the command below
to add a function to enter a container easily:
::

   cat >>~/.bashrc << 'EOF'
   ne () {
     pid=$(docker inspect --format '{{.State.Pid}}' $1)
     env SHELL='/bin/bash' sudo -E nsenter --target $pid --mount --uts --ipc --net --pid
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
we will use it later. In this example it should be:
::

   echo 'export DOCKER_INET=172.17.42.1' >> ~/.bashrc

Remember to replace ``172.17.42.1`` with the output on your system!

Reload ``~/.bashrc``:
::

   source ~/.bashrc

.. _Docker: http://docker.com
.. _nsenter: http://blog.docker.com/tag/nsenter/
