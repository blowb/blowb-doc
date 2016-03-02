Preface
=======

What is This Manual About?
--------------------------

.. index:: Internet app, Blowb, free software

This manual consists of instructions to set up integrated Internet services using existing `free software`_ for you,
your family and/or your organization under a framework using Docker. Before reading this manual, make sure you
understand the basics of GNU/Linux commands (or a different POSIX system such as Mac OS X, FreeBSD). Server setup
knowledge is recommended but not required. By following the instructions in this manual, you should be able to set up an
integrated system running multiple server software---we will refer them as "Internet apps" throughout this manual. In
addition, you can also use this manual as a reference. For instance, if you follow some other instructions to deploy a
server with Docker, or to set up some of the software mentioned in this manual, this manual may be helpful.

This manual is the main work of the Blowb project, and is mainly authored by `Hong Xu <http://www.topbug.net>`__. The
latest version of this manual is available online at http://www.blowb.org .

What is the Blowb Project?
--------------------------

.. include:: what-is-blowb.rst

Why the Blowb Project?
----------------------

There are two major reasons: technical reasons and social reasons.

Technical Reasons
~~~~~~~~~~~~~~~~~

Docker is an emerging technology which can isolates service better than most traditional server setups. However, to the
author's knowledge, there is still no thorough document at this point of time which explains how to deploy integrated
service using Docker. Thus, this manual was created in order to let people who want to deploy service using Docker have
a guide to follow and a reference to look up.


Social Reasons
~~~~~~~~~~~~~~

.. index:: cloud, privacy, censorship

Many organizations and individuals use third party servers to serve some of their work, e.g., cloud-based file
synchronization, cloud-based office suite, etc. Despite the convenience, this practice causes many issues---mainly
privacy and censorship issues (see :doc:`appendices/why-our-server` for more detailed descriptions). To help solve this
issue, this manual was written to make server setup easier thus encourages people to deploy service on their own servers
instead of using third party servers.

.. _free software: https://www.gnu.org/philosophy/free-sw.html
