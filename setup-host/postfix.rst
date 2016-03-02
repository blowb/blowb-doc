Configure Postfix
=================

.. index:: Postfix
   mail transport agent
   see: MTA; mail transport agent
   see: email; SMTP
   SMTP
   seealso: SMTP; mail transport agent
   seealso: mail transport agent; SMTP

`Postfix`_ is a popular mail server and is the default mail transport agent (MTA) on RHEL/CentOS 7. Postfix on the host
system will serve two purposes: sending admin notification mails to our email inbox, and acting as the mailer for the
Internet services that we will install later (such as registering email confirmation, notification, etc). In this
section, we will configure a minimal Postfix instance, e.g. no associated domain, no incoming mails from outside
accepted.

Install and Enable Postfix
--------------------------

Postfix is installed and enabled by default on RHEL/CentOS 7. Just in case, we can check whether Postfix is installed
and running by running the following two commands:
::

   rpm -qa | grep postfix
   systemctl status postfix

Or just simply run the following commands to install and enable Postfix:
::

   sudo yum install postfix
   sudo systemctl start postfix
   sudo systemctl enable postfix

Configure Postfix for Admin
---------------------------

We need to set up all mails sent to the root user to be sent to our own inbox. ``/etc/aliases`` is the file where
Postfix uses to set up mail aliases for users on the system. We may need to inspect this file to ensure that there are
no strange aliases (e.g. root has already been aliased to a different person). Then after replacing ``me@example.com``
with your email address, run the following command on bash to add root as the alias of your email address and make the
changed aliases file take effects:
::

   sudo bash -c "echo 'root:  me@example.com' >>/etc/aliases"
   sudo newaliases

Send root a mail to see whether it works:
::

   sendmail -t root <<'EOF'
   From: test@example.com
   Subject: This is a test

   The test on alias works!

   .
   EOF

If configured correctly, you should have receives an email from ``test@example.com`` (Remember to
check your spam box if you did not receive).

.. index::
   single: Docker; docker0

Configure Postfix for Software Running in Docker Containers
-----------------------------------------------------------

There are two changes need to be made on Postfix.

1. Exposing Postfix to the docker network, that is, Postfix must be configured to bind to localhost as
   well as the docker network.

2. Accepting all incoming connections which come from any Docker containers.

In this section we will do manual editing of configuration files of Postfix. Edit ``/etc/postfix/main.cf``:
::

   sudo $EDITOR /etc/postfix/main.cf

To achieve point 1 listed above, search this file for the entry ``inet_interfaces``. Replace the line with:

.. code-block:: none

   inet_interfaces = localhost, <echo $HOST_ADDR>

where ``<echo $HOST_ADDR>`` should be replaced with the output of ``echo $HOST_ADDR`` run on bash.

To achieve point 2, search this file for ``mynetworks``. The whole docker network as well as localhost should be added
to ``mynetworks``. If the output of ``ifconfig docker0`` shows a netmask of ``255.255.0.0`` (which is the default case),
add this following line below the commented ``mynetworks`` lines:

.. code-block:: none

   mynetworks = localhost, <echo $HOST_ADDR | awk -F. '{print $1 "." $2 ".0.0/16"}'>

Where ``<echo $HOST_ADDR | awk -F. '{print $1 "." $2 ".0.0/16"}'>`` is the corresponding output on bash.

Save the configuration file and restart Postfix:
::

   sudo systemctl restart postfix

.. index:: firewall, firewalld
   single: Docker; docker0

If the firewall is enabled, we need to make ``docker0`` a trusted network (you probably have done it in
:doc:`dnsmasq`; in this case, there is no need to execute them again and you can just skip them):
::

   sudo firewall-cmd --permanent --zone=trusted --change-interface=docker0
   sudo firewall-cmd --reload

To test whether it works within a docker container, run the following command to start a test docker
container:
::

   docker run -t -i --rm debian /bin/bash

We should be running bash in the docker container now. Run the commands below after replacing
``me@example.com`` with your email address:
::

   YOUR_EMAIL=me@example.com
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

Run the following commands to connect to the Postfix server and send out the email:
::

   apt-get update && apt-get install -y netcat
   nc <echo $HOST_ADDR> 25 <sendmail.txt

If successful, we should be able to receive an email from ``test@example.com``. If you didn't receive the email, you
should check the spam folder first. Now exit the bash in the container and the testing container should be automatically
deleted:
::

   exit # quit the bash in the docker container

One More Test
-------------

To be ensure that this Postfix instance is not acting as an `open relay`_ on the Internet, test from
a different computer to see that whether Postfix accepts incoming connections from outside:
::

   telnet your_server_address 25

.. index:: netcat, telnet
   see: nc; netcat

Here we can also use the ``nc`` command to perform the test; using telnet is just easier for Windows users.

If the output is similar to the following:

.. code-block:: none

   220 host_name ESMTP Postfix

.. index:: spam

Then something's wrong. Please do not ignore this issue---it can make the server a spam machine.

.. _Postfix: http://www.postfix.org
.. _open relay: https://en.wikipedia.org/wiki/Open_mail_relay
.. _netcat: https://en.wikipedia.org/wiki/Netcat
