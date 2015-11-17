Preface
=======

What is the Blowb Project?
--------------------------

.. include:: what-is-blowb.rst

Why the Blowb Project?
----------------------

There are two major reasons: technical reasons and political reasons.

Technical Reasons
~~~~~~~~~~~~~~~~~

Docker is an emerging technology which can isolates service better. However, there is no thorough document at this point
which explains how to deploy integrated service using Docker. This document was written so that people who want to
deploy service using Docker can have a guide to follow and a reference to look up.


Political Reasons
~~~~~~~~~~~~~~~~~

Many organizations and individuals use third party servers to serve some of their work, e.g. cloud file synchronization,
cloud-based office suite, etc. This practice causes some problems -- mainly privacy and censorship issues (see
:doc:`appendices/why-our-server` for a more detailed description). This document was written to make server setup easier
thus encourages people to deploy service on their own servers.

How to Use This Document
------------------------

This document consists of instructions to set up a relatively comprehensive set of Internet services using existing
`free software`_ for you, your family and/or your organization under a framework using Docker. Basic knowledge of
GNU/Linux (or a different POSIX system such as OS X, FreeBSD) command line is required. Server setup knowledge is
recommended but not required. you should be able to set up an integrated system running multiple server software
following this document, but you can also use this document as a reference if you follow a different document to set up
some of the software mentioned in this document.

.. _free software: https://www.gnu.org/philosophy/free-sw.html
