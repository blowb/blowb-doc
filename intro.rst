..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Blowb is a free document project which aims to help individuals and organizations set up servers which run
free/open-source Internet and/or intranet services. The Blowb project also promotes open `federation
<https://en.wikipedia.org/wiki/Federation_(information_technology)>`_ protocols and software whenever applicable.

.. _privacy-censorship:

Privacy and Censorship Concerns Rise at the Age of the Internet
---------------------------------------------------------------

At the age of the Internet, we use Internet services everyday: We use Google Hangout to communicate; we use Facebook to
share stories; we use Chrome Sync to synchronize browser bookmarks. They are pretty cool, but do you know

  - that they collect your data, even private data, for the purpose to "improve your experience as a user";
  - that they tie you to their platforms and your friends have to be also tied to the platform to be with you;
  - that they control what stories you "should" publish and what stories you "should not" publish.

Privacy and free speech are threatened.

Organizations and Working groups are Subjugated to Proprietary Software and Network Service
-------------------------------------------------------------------------------------------

Many small organizations and working groups use proprietary software and file formats to collaborate. This leads to the
fact that they are largely limited by the software and formats they use.

  - If their work is not done on their own servers, the points in :ref:`privacy-censorship` apply.
  - They are not able to extend the software they use to fit in their situation by themselves or hiring people -- that
    is, they do not control the software they run.
  - If the companies which creates the software and formats are gone, they will either become unsupported, or migrate to
    a new system which is usually expensive in the sense of time, money and quality.

Solve the Problem using Free and Federated Software
---------------------------------------------------

The problem **can be solved**. There are many network related `free software`_ projects which cover almost all commonly
used Internet and intranet services:

  - GNU Social for decentralized and federated social networking,
  - Mozilla Sync for synchronizing your web browsers,
  - ownCloud for file, contact and calendar synchronization,
  - Prosody and other free XMPP software for instant messaging,
  - ... (a longer list is `available <https://en.wikipedia.org/wiki/List_of_free_software_web_applications>`_)

However, by the time this document was written, there were no comprehensive documents showing how to set up these
software systematically. For this reason, I started the Blowb project, which is a free document project on setting up
these free software more integrally than each individual server software's own document.

This document consists of instructions to set up a relatively comprehensive set of Internet services using existing free
software for you, your family and/or your organization. Basic knowledge of GNU/Linux (or a different POSIX system such
as OS X, FreeBSD) command line is required. Server setup knowledge is recommended but not required. you should be able
to set up an integrated system running multiple server software following this document, but you can also use this
document as a reference if you follow a different document to set up some of the software mentioned in this document.

.. _free software: https://www.gnu.org/philosophy/free-sw.html
