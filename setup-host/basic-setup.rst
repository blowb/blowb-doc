Basic Setup and Preparation
===========================

Create an Admin User
--------------------

.. index:: root user

If an admin user has not been set up on the server, we probably would create one to avoid using the root user to
maintain. We can run the following command to create an admin user, after replacing ``<admin_user_name>`` with your
favorite admin user name, such as ``admin``:
::

   useradd -g wheel <admin_user_name>  # create the admin user
   passwd <admin_user_name>   # set up the password

We put the account to wheel group, so this account can use ``sudo`` to run some high privilege
commands. Now we can switch to the admin user by running:
::

   su <admin_user_name>

Update the System
-----------------

.. index:: yum

It is essential for security and stability to keep the software packages up-to-date. Run the command below to update all
system packages:
::

   sudo yum update

If this command fails, you should go back and check whether the admin account is set up correctly.

Install Admin Tools
-------------------

.. index:: ed, netcat, telnet
   see: wget; GNU
   single: GNU; bash
   single: GNU; wget

We probably also need to install some utilities:
::

   sudo yum install bash-completion ed nc telnet wget

.. index:: Vim

We also need to set up a favorite terminal editor. If you are relatively new to GNU/Linux, I would suggest you to try
`Vim`_, which is an enhanced version of the POSIX standard vi. It has a steep but short learning curve, but once you get
used to it, you would become more efficient to edit configuration files than most other editors. To install Vim, run:
::

   sudo yum install vim-enhanced

.. index:: vi

Or simply use the ``vi`` command if you still want to use a vi style editor but not the full Vim.

.. index::
   single: GNU; nano
   see: nano; GNU

In the case you really don't want to learn vi key bindings, you may want to take a look at `GNU Nano`_. To install GNU
Nano, run:
::

   sudo yum install nano

You can use any other terminal editors as you want. Next, we should set up the ``EDITOR`` environment variable to your
favorite editor command.

- If you use Vim:
  ::

     echo 'export EDITOR=vim' >> ~/.bashrc

- If you use vi (actually it is the small version of Vim on CentOS):
  ::

     echo 'export EDITOR=vi' >> ~/.bashrc

- To use GNU Nano:
  ::

     echo 'export EDITOR=nano' >> ~/.bashrc

- Other editors:
  ::

     echo 'export EDITOR=command_of_the_editor' >> ~/.bashrc

Store Logs Persistently
-----------------------

.. index:: systemd
   see: journald; systemd

By default the logs are only stored in memory and cleared after a reboot. To preserve the logs after each reboot, we
have to set a journald option. Edit the file ``/etc/systemd/journald.conf``:
::

   sudo $EDITOR /etc/systemd/journald.conf

Uncomment the line ``#Storage=auto``, and change ``auto`` to ``persistent``. Save the change and exit the editor.
Alternatively, the following command can be used to apply the change:
::

   sudo sed -i 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf

Reboot
------

To safely assure everything set up in this section to be applied, reboot the system:
::

   sudo reboot

.. _Vim: http://www.vim.org/
.. _GNU Nano: http://www.nano-editor.org/
