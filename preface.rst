..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

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
which explains how to set up integrated service using Docker. This document was written so that people who want to set
up a server using Docker can have a guide to follow and a reference to look up.


Political Reasons
~~~~~~~~~~~~~~~~~

Many organizations and individuals use third party servers to serve some of their work, e.g. cloud file synchronization,
cloud-based office suite, etc. This practice causes some problems -- mainly privacy and censorship issues (see
:doc:`appendices/why-our-server` for a more detailed description). This document was written to make server setup easier
thus encourages people to set up their own servers.

How to Use This Document
------------------------

This document consists of instructions to set up a relatively comprehensive set of Internet services using existing
`free software`_ for you, your family and/or your organization under a framework using Docker. Basic knowledge of
GNU/Linux (or a different POSIX system such as OS X, FreeBSD) command line is required. Server setup knowledge is
recommended but not required. you should be able to set up an integrated system running multiple server software
following this document, but you can also use this document as a reference if you follow a different document to set up
some of the software mentioned in this document.

.. _free software: https://www.gnu.org/philosophy/free-sw.html
