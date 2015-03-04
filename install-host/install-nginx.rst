Install Nginx
=============

To install nginx:
::

    # install epel if not yet
    sudo yum install epel-release
    sudo yum install nginx

Start nginx on boot:
::

    sudo systemctl enable nginx

If needed create a dummy SSL/TLS key pair for nginx:
::

    sudo openssl req -x509 -nodes -days 3000 -newkey rsa:2048 -keyout /etc/pki/tls/private/dummy.key -out /etc/pki/tls/certs/dummy.crt
