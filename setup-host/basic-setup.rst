Basic Setup and Preparation
===========================

If you haven't get an admin user account set up on your server, you probably want to create one to
avoid using root to maintain. You can run the following command, after replacing
``<admin_user_name>`` with your favorite admin user name, such as ``admin``:
::

   useradd -g wheel <admin_user_name>  # create the admin user
   passwd <admin_user_name>   # set up the password

We put the account to wheel group, so this account can use ``sudo`` to run some high privilege
commands. Now you can switch to the admin user by running:
::

   su <admin_user_name>

Probably you want to make sure software packages are up-to-date. Run the command below to update all
system packages:
::

   sudo yum update

If this command fails, you should go back and check whether the admin account is set up correctly.

We probably also need to install some utilities:
::

   sudo yum install bash-completion ed nc telnet

We also need to set up a favorite terminal editor. If you are relatively new to GNU/Linux, I suggest you to try `Vim`_,
which is an enhanced version of the POSIX standard vi. It has a steep but short learning curve for editing configuration
files, but once you get used to it, you would become more efficient to edit configuration files than in the past. To
install Vim, run:
::

   sudo yum install vim-enhanced

Or simply use the ``vi`` command if you still want to use a vi style editor but not the full Vim.

In the case you really don't want to learn vi key-binding, you may want to take a look at `GNU Nano`_. To install GNU
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

     echo 'export EDITOR=command_of_the_editor >> ~/.bashrc

To safely assure everything set up in this section to be applied, reboot the system:
::

   sudo reboot

.. _Vim: http://www.vim.org/
.. _GNU Nano: http://www.nano-editor.org/
