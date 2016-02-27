Set up Dnsmasq
==============

Install And Configure Dnsmasq
-----------------------------

`Dnsmasq <http://www.thekelleys.org.uk/dnsmasq/doc.html>`_ can be used as a lightweight DNS server. We will use dnsmasq
to store the address of each Docker container we will set up later.

To install dnsmasq:
::

   sudo yum install dnsmasq

We then need to configure dnsmasq. Edit the configuration file ``/etc/dnsmasq.conf``:
::

   sudo $EDITOR /etc/dnsmasq.conf

Search for the option ``interface`` in the file, uncomment the line, and change it to the following:

.. code-block:: cfg

   interface=docker0

Search for the option ``domain-needed`` and uncomment it, since we have all Docker container names without dots.

Save the file and exit.

We can now start dnsmasq:
::

   sudo systemctl enable dnsmasq
   sudo systemctl start dnsmasq

If the firewall is enabled (you can check it by executing ``systemctl status firewalld``), we need to make ``docker0`` a
trusted network:
::

   sudo firewall-cmd --permanent --zone=trusted --change-interface=docker0
   sudo firewall-cmd --reload

To test whether dnsmasq is accessible from a Docker container, run the following command to run a shell in Docker
container:
::

   docker run -t -i --rm debian /bin/bash

In this shell:
::

   apt-get update && apt-get install -y --no-install-recommends dnsutils
   dig @<echo $HOST_ADDR> www.blowb.org

where ``<echo $HOST_ADDR>`` is the output of ``echo $HOST_ADDR`` on the bash shell on the host system. If the DNS record
of ``www.blowb.org`` is shown, then ``dnsmasq`` is correctly set up. Exit the shell in the container by press
``Ctrl-D``.

Auto Update DNS Record of Docker Containers
-------------------------------------------

We need to automatically update Docker container DNS records when a container changes its IP address.

We have prepared a script ``update-dnsmasq.sh`` to do auto updating, and a systemd unit file to run the script as a
daemon (can be viewed in :doc:`../appendices/update-dnsmasq`). The script checks the IP addresses of all running
containers every period of time (10s by default). If the change of an IP address is detected, it will update the
configuration files in ``/etc/dnsmasq.d`` and restart ``dnsmasq``. To download the relevant files and run this script:
::

   sudo wget -O /usr/local/bin/update-dnsmasq.sh \
    http://docs.blowb.org/_downloads/update-dnsmasq.sh
   sudo chmod +x /usr/local/bin/update-dnsmasq.sh
   sudo wget -O /usr/lib/systemd/system/update-dnsmasq.service \
    http://docs.blowb.org/_downloads/update-dnsmasq.service
   sudo systemctl enable update-dnsmasq && sudo systemctl start update-dnsmasq
