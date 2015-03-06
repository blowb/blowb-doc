Install Docker
==============

`Docker`_ is an essential software in Blowb. Most of our services will be installed into a docker
container for better isolation.

Run the following command to install docker:
::

   yum install docker

Make docker start at boot:
::

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
    pid=$(docker inspect --format {{.State.Pid}} $1)
    nsenter --target $pid --mount --uts --ipc --net --pid
   }
   EOF

.. _Docker: http://docker.com
.. _nsenter: http://blog.docker.com/tag/nsenter/
