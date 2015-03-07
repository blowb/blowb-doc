Basic Setup and Preparation
===========================

If you haven't get an admin user account set up on your server, you probably want to create one to
avoid using root to maintain. You can run the following command, after replacing
``<admin_user_name>`` with your favorite admin user name, such as ``admin``:
::

   useradd -g wheel <admin_user_name>  # create the admin user
   passwd <admin_user_name>   # set up the password

We put the account to wheel group, so this account can use ``sudo`` to run some high privilege
commands. Now you can switch to the admin user by run:
::

   su <admin_user_name>

Probably you want to make sure software packages are up-to-date. Run the command below to update all
system packages:
::

   sudo yum update

If this command fails, you should go back and check whether the admin account is set up correctly.

You may want to install some helpful utilities (Optional):
::

   sudo yum install bash-completion nc telnet vim-enhanced

To safely assure everything set up in this section to be applied, reboot the system.
