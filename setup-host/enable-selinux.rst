..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Enable SELinux (Optional but Recommended)
=========================================

`SELinux`_ is a Linux kernel security module which provides `mandatory access controls`_. It is
highly recommended to enable SELinux on your system, especially a GNU/Linux distribution like CentOS
which provides good out-of-box integration with SELinux.

To install relevant packages:
::

   sudo yum install policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted \
        libselinux-utils setroubleshoot-server setools setools-console mcstrans

To check the status of SELinux on your system, you can run the command below:
::

   getenforce

You may have the following 3 possible output:

- **Disabled**. Your SELinux module is disabled. You can edit ``/etc/selinux/config`` to change to
  permissive mode:

  ::

     sudo vi /etc/selinux/config

  Modify the ``SELINUX`` entry from ``disabled`` to ``permissive`` and reboot. Now your
  ``getseforce`` output should be ``permissive``. If the output is not permissive, go back and check
  whether anything went wrong. Then you can follow the instructions of the ``permissive`` part.

- **Permissive**. Your SELinux module is in permissive mode. Before you put SELinux into enforcing
  mode, you **must** check there is no SELinux errors that may prevent you from booting up. Run the
  following command to check any possible SELinux errors:

  ::

     sudo journalctl -b 0 | grep -i selinux

  Briefly browse the output and make sure there is no strange errors. Then run the following command
  and modify the ``SELINUX`` entry from ``permissive`` to ``enforcing``:
  ::

     sudo vi /etc/selinux/config

  Reboot the system. Now you should have ``getenforce`` command outputs "enforcing".

- **Enforcing**. You have already enabled SELinux. No additional work need to be done.

.. _SELinux: http://selinuxproject.org/page/Main_Page
.. _mandatory access controls: https://en.wikipedia.org/wiki/Mandatory_access_control
