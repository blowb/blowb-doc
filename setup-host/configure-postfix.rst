Configure Postfix
=================

Postfix on the host will serve two purposes: sends admin notification mails to your email inbox, and
acts as the mailer for the Internet services we will install later (such as registering email
confirmation, notification, etc).

Postfix is installed and started by default on CentOS. Just in case, you can check whether postfix
is installed and running by running the following two commands:
::

   rpm -qa | grep postfix
   systemctl status postfix

Or just simply run:
::

   sudo yum install postfix
   sudo systemctl start postfix
   sudo systemctl enable postfix

We need to set up all mails which the root user is supposed to receive to be sent to you.
``/etc/aliases`` is the file where postfix uses to set up mail aliases for users on the system. You
may inspect this file to ensure that there are no strange aliases (e.g. root has already been
aliased to a different person). Then after replacing ``you@example.com`` with your email address,
Or run the following command on bash to add root as the alias of you and make the changed aliases
file take effects:
::

   sudo bash -c "echo 'root:  you@example.com' >>/etc/aliases"
   sudo newaliases
