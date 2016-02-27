Set up the Host System on Other GNU/Linux Distributions
=======================================================

This chapter has guided you to prepare the host system on RHEL/CentOS, but it is also possible to set up the host on a
different GNU/Linux distribution, as long as the following requirements are met:

- Ed, dnsmasq, Docker, GNU sed, netcat, and GNU wget are available.
- A mail transfer agent (MTA) is available.
- The scripts introduced in :doc:`dnsmasq` can be installed, thus the availability of systemd is recommended. If systemd
  is not available, the systemd unit file introduced in :doc:`dnsmasq` must be replaced by an equivalent configuration
  file for the available service manager.

After the host system is set up, the following criteria must be met to proceed to the next chapter:

- Ed, GNU sed, netcat and GNU wget are installed. An admin user account is set up. (Corresponding to :doc:`basic-setup`)
- Docker is up and running. (Corresponding to :doc:`docker`)
- An MTA is up and running and listens on port 25 on ``docker0`` and localhost. A process in a Docker container must be
  able to send out mails via port 25 of the host. (Corresponding to :doc:`postfix`)
- Dnsmasq is up and running, and its DNS configuration is updated automatically when a Docker container is created or
  its IP address has changed. (Corresponding to :doc:`dnsmasq`)

A mandatory access control system, such as SELinux and Apparmor, is highly recommended to be enabled if available for
your distribution.
