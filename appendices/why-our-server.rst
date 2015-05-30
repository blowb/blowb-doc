..  Copyright (c) 2015 Hong Xu <hong@topbug.net>

..  This file is part of Blowb.

    Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later
    version.

    Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Blowb.  If not, see
    <http://www.gnu.org/licenses/>.

Why should we set up our own server?
====================================

Privacy and Censorship Concerns Rise at the Age of the Internet
---------------------------------------------------------------

At the age of the Internet, we use Internet services everyday: We use Google Hangout to communicate; we use Facebook to
share stories; we use Chrome Sync to synchronize browser bookmarks. They are pretty cool, but do you know

  - that they collect your data, even private data, for the purpose to "improve your experience as a user";
  - that they tie you to their platforms and your friends have to be also tied to the platform to be with you;
  - that they control what stories you "should" publish and what stories you "should not" publish.

Privacy and free speech are threatened.

Organizations and Working Groups are Subjugated to Proprietary Network Service and Software
-------------------------------------------------------------------------------------------

Many small organizations and working groups use proprietary network service (often coupled with proprietary software) to
collaborate. This leads to the fact that they are largely limited by the software they use.

  - They are not able to extend the service or software they use to fit in their situation by themselves or hiring
    people -- that is, they do not control the software they run.
  - If the companies which creates the proprietary network service and software (and maybe formats) are gone, they will
    either become unsupported, or migrate to a new system which is usually expensive in the sense of time, money and
    quality.

Solve the Problem by Setting up Our Own Server
----------------------------------------------

The problem **can be solved**. There are many network related `free software`_ projects which cover almost all commonly
used network services:

  - GNU Social for decentralized and federated social networking,
  - Mozilla Sync for synchronizing your web browsers,
  - ownCloud for file, contact and calendar synchronization,
  - Prosody and other free XMPP software for instant messaging,
  - ... (a longer list is `available <https://en.wikipedia.org/wiki/List_of_free_software_web_applications>`_)

It looks like it is completely possible to set up our own server. However, by the time this document was written, there
were no comprehensive documents showing how to set up these software integrally. For this reason, the Blowb project was
started, which is a free document project on setting up these free software more integrally than each individual server
software's own document.

.. _free software: https://www.gnu.org/philosophy/free-sw.html
