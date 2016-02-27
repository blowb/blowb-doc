Technical Overview
==================

The whole system will be built on `GNU/Linux`_, and `Docker`_ will be used for deployment of Internet apps. We will
deploy most apps in Docker containers, which run on top of the host system. We use Docker for the reason that a Docker
container can isolate the app in it from other parts of the system, which usually leads to easy deployment, and better
security. A typical deployment structure for an app is illustrated in :numref:`overview-diagram`.

.. _overview-diagram:

.. graphviz::
   :alt: Overview of the deployment structure.
   :caption: Overview of the deployment structure is shown.

   digraph structure {
     graph[overlap=false, splines=true]
     node[shape=record]

     "app" [label="Internet App"]
     "client" [label="User (Client)"]
     "data" [label="Data Container"]
     "mariadb" [label="MariaDB"]
     "nginx" [label="Nginx"]
     "openldap" [label="OpenLDAP"]
     "postfix" [label="Postfix (Sitting on the Host)"]

     "client" -> "nginx" [label="Sends Request to"]
     "nginx" -> "app" [label="Forwards Request to"]
     "app" -> "data" [label="Stores Data Files in"]
     "app" -> "mariadb" [label="Stores Data in"]
     "app" -> "openldap" [label="Authenticates via"]
     "app" -> "postfix" [label="Sends Email via"]
   }

As shown in :numref:`overview-diagram`, software in each box runs inside a Docker container, except for Postfix which
runs on the host. Containers locate each other via the dnsmasq server on the host (not shown in
:numref:`overview-diagram`). Note that not all Internet apps have the complete structure as shown in
:numref:`overview-diagram`, e.g., the XMPP/Jabber server software Prosody is not a web service thus Nginx is not part of
the game---users send requests directly to the Prosody instance.

Throughout this manual, `GNU Bash`_ is assumed to be the shell used on the host.

.. _Docker: https://www.docker.com
.. _GNU Bash: https://www.gnu.org/software/bash/
.. _GNU/Linux: http://www.getgnulinux.org/en/
