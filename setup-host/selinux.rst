Enable SELinux (Optional but Recommended)
=========================================

.. index:: SELinux, mandatory access control
   see: MAC; mandatory access control
   seealso: SELinux; mandatory access control
   seealso: SELinux; AppArmor
   seealso: AppArmor; SELinux
   seealso: AppArmor; mandatory access control
   seealso: mandatory access control; SELinux
   seealso: mandatory access control; AppArmor

`SELinux`_ is a Linux kernel security module which provides `mandatory access controls`_. It is highly recommended to
enable SELinux on your system, especially a GNU/Linux distribution such as RHEL/CentOS which provides good out-of-box
integration with SELinux.

To install relevant packages:
::

   sudo yum install policycoreutils policycoreutils-python selinux-policy \
    selinux-policy-targeted libselinux-utils setroubleshoot-server setools \
    setools-console mcstrans

To check the status of SELinux on the system, we can run the command below:
::

   getenforce

We may have the following 3 possible output.

- **Disabled**. The SELinux module is disabled. We can edit ``/etc/selinux/config`` to change to permissive mode:
  ::

     sudo vi /etc/selinux/config

  Modify the ``SELINUX`` entry from ``disabled`` to ``permissive`` and reboot. Now the
  ``getseforce`` output should be ``permissive``. If the output is not permissive, go back and check
  whether anything went wrong. Then we can follow the instructions of the ``permissive`` part.

- **Permissive**. The SELinux module is in permissive mode. Before changing SELinux into enforcing mode, we should
  ensure there is no SELinux errors that may prevent the system from booting up. Run the following command to check any
  possible SELinux errors:
  ::

     sudo journalctl -b 0 | grep -i selinux

  Briefly browse the output and make sure there is no relevant error. Then run the following command
  and modify the ``SELINUX`` entry from ``permissive`` to ``enforcing``:
  ::

     sudo vi /etc/selinux/config

  Reboot the system. Now the ``getenforce`` command should output ``enforcing``.

- **Enforcing**. You have already enabled SELinux. No additional work need to be done.

.. _SELinux: http://selinuxproject.org/page/Main_Page
.. _mandatory access controls: https://en.wikipedia.org/wiki/Mandatory_access_control
