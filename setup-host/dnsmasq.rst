..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Set up Dnsmasq
==============

Install And Configure Dnsmasq
-----------------------------

`Dnsmasq <http://www.thekelleys.org.uk/dnsmasq/doc.html>`_ can be used as a lightweight DNS server. We will use dnsmasq
to store the address of each Docker container we will set up later.

To install dnsmasq:
::

   sudo yum install dnsmasq

We then need to configure dnsmasq. Open the file ``/etc/dnsmasq.conf`` with your favorite editor:
::

   sudo $EDITOR /etc/dnsmasq.conf

Search for the option ``interface``, uncomment the line, and change it to the following:

.. code-block:: cfg

   interface=docker0

Search for the option ``domain-needed`` and uncomment it, since we have all Docker container names without dots.

Save the file and exit.

We can now start dnsmasq:
::

   sudo systemctl enable dnsmasq
   sudo systemctl start dnsmasq

To test whether dnsmasq is accessible from a Docker container, run the following command to run a shell in Docker
container:
::

   docker run -t -i --rm debian /bin/bash

In this shell:
::

   apt-get update && apt-get install -y --no-install-recommends dnsutils
   dig @<echo $HOST_ADDR> www.blowb.org

Where ``<echo $HOST_ADDR>`` is the output of ``echo $HOST_ADDR`` on the bash shell on your host. If the DNS record
of ``www.blowb.org`` is shown, ``dnsmasq`` is correctly set up. Exit the shell in the container by press ``Ctrl-D``.

Auto Update DNS Record of Docker Containers
-------------------------------------------

We need to automatically update Docker container DNS records when a container changes its IP address.

The Blowb project has prepared a script ``update-dnsmasq.sh`` to do auto updating, and a systemd unit file to run the
script as a daemon. The script checks the IP addresses of all running containers every period of time (10s by default).
If a change of IP address(es) is detected, it will update the configuration files in ``/etc/dnsmasq.d`` and restart
``dnsmasq``.  To download the relevant files and run this script:
::

   sudo wget -O /usr/local/bin/update-dnsmasq.sh \
    http://docs.blowb.org/_downloads/update-dnsmasq.sh
   sudo chmod +x /usr/local/bin/update-dnsmasq.sh
   sudo wget -O /usr/lib/systemd/system/update-dnsmasq.service \
    http://docs.blowb.org/_downloads/update-dnsmasq.service
   sudo systemctl enable update-dnsmasq && sudo systemctl start update-dnsmasq
