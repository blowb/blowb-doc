..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Configure Postfix
=================

`Postfix`_ is a mail server. Postfix on the host system will serve two purposes: sends admin
notification mails to your email inbox, and acts as the mailer for the Internet services we will
install later (such as registering email confirmation, notification, etc). In this section, we will
configure a minimal postfix instance, e.g. no associated domain, no incoming mails from outside
accepted.

Install and Enable Postfix
--------------------------

Postfix is installed and enabled by default on CentOS. Just in case, you can check whether postfix
is installed and running by running the following two commands:
::

   rpm -qa | grep postfix
   systemctl status postfix

Or just simply run the following commands to install and enable postfix:
::

   sudo yum install postfix
   sudo systemctl start postfix
   sudo systemctl enable postfix

Configure Postfix for Admin
---------------------------

We need to set up all mails which the root user is supposed to receive to be sent to you.
``/etc/aliases`` is the file where postfix uses to set up mail aliases for users on the system. You
may inspect this file to ensure that there are no strange aliases (e.g. root has already been
aliased to a different person). Then after replacing ``you@example.com`` with your email address,
Or run the following command on bash to add root as the alias of you and make the changed aliases
file take effects:
::

   sudo bash -c "echo 'root:  you@example.com' >>/etc/aliases"
   sudo newaliases

Send root a mail to see if it works:
::

   sendmail -t root <<'EOF'
   From: test@example.com
   Subject: This is a test

   The test on alias works!

   .
   EOF

If configured correctly, you should have receives an email from ``test@example.com`` (Remember to
check your spam box).

Configure Postfix for Software Running in Docker Containers
-----------------------------------------------------------

There are two changes need to be made on postfix:

1. Expose postfix to the docker network, that is, postfix must be configured to bind to localhost as
   well as the docker network;

2. Accept all incoming connections which come from any docker container.

In this section we will do manual editing of configuration files of postfix. Open
``/etc/postfix/main.cf`` with your favorite editor, e.g.
::

   sudo $EDITOR /etc/postfix/main.cf

To achieve point 1 listed above, search the file for the entry ``inet_interfaces``. Replace the line
with:

.. code-block:: none

   inet_interfaces = localhost, <echo $DOCKER_ADDR>

where ``<echo $DOCKER_ADDR>`` should be replaced with your output of ``echo $DOCKER_ADDR`` when run
on bash.

To achieve point 2, search this file for ``mynetworks``. The whole docker network as well as
localhost should be added to ``mynetworks``. If your ``ifconfig docker0`` has a netmask of
``255.255.0.0`` (which is the default case), add this following line below the commented
``mynetworks`` lines:

.. code-block:: none

   mynetworks = localhost, <echo $DOCKER_ADDR | awk -F. '{print $1 "." $2 ".0.0/16"}'>

Where ``<echo $DOCKER_ADDR | awk -F. '{print $1 "." $2 ".0.0/16"}'>`` is the corresponding output on
bash.

Save the configuration file and restart postfix:
::

   sudo systemctl restart postfix

To test whether it works within a docker container, run the following command to start a test docker
container:
::

   docker run -t -i --rm debian /bin/bash

You should be running bash in the docker container now. Run the commands below after replacing
``you@example.com`` with your email address:
::

   YOUR_EMAIL=you@example.com
   cat > sendmail.txt <<EOF
   HELO x
   MAIL FROM: test@example.com
   RCPT TO: $YOUR_EMAIL
   DATA
   From: test@example.com
   To: $YOUR_EMAIL
   Subject: This is a test

   The test is successful

   .
   quit
   EOF

Run the following commands to starts connect
to the postfix server:
::

   apt-get update && apt-get install -y netcat
   nc <echo $DOCKER_ADDR> 25 <sendmail.txt

If successful, you should be able to receive an email in your inbox from ``test@example.com``. Also
check your spam folder if you didn't receive the email. Now exit the bash in the container and
the testing container should automatically be deleted:
::

   exit # quit the bash in the docker container

One More Test
-------------

To be ensure that this postfix instance is not acting as an `open relay`_ on the Internet, test from
a different computer to see that whether postfix accepts incoming connections from outside:
::

   telnet your_server_address 25

(You can also use `netcat`_ to perform the test; using telnet is just easier for Windows users)

If you see some output similar to the following:

.. code-block:: none

   220 host_name ESMTP Postfix

Then you must have done something wrong. Please don't ignore this issue and go back to double check
-- this issue can make your server a spam machine.

.. _Postfix: http://www.postfix.org
.. _open relay: https://en.wikipedia.org/wiki/Open_mail_relay
.. _netcat: https://en.wikipedia.org/wiki/Netcat
