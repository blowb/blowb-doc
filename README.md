# The Blowb Project

Blowb is a free document project which aims to help individuals and organizations set up servers
which run free/open-source Internet and/or intranet services. The Blowb project also promotes open
[federation](https://en.wikipedia.org/wiki/Federation_(information_technology)) protocols and
software whenever applicable.

The project is currently under development, but you are free to play with it.

Please visit http://www.blowb.org to read the document.

## Obtain the Latest Source Code

You can always get the latest source code using [git][]:

    git clone --recursive https://gitlab.com/blowb/blowb.git

Or download through [this link](https://gitlab.com/blowb/blowb/repository/archive.tar.gz).

Visit the [project page on GitLab](https://gitlab.com/blowb/blowb) for more details.

## Build the Document

To build the document, first please follow [this link](http://sphinx-doc.org/install.html) to
install [Sphinx][], which is the main tool to build the document. [GNU Make][] or a compatible
[Make][] program is also needed. If you need to generate the diagrams, you must to have [Graphviz][]
installed. [LaTeX][] is required if you want to generate the PDF version of the document.

Then we need to download the theme files if you are going to use the same theme as
[the Blowb online doc](http://docs.blowb.org). If you used [git][] to obtain the source, please make
sure the theme submodule is update to date:

    git submodule update --init

If you did not use git to obtain the source code, please download the
[theme files](https://github.com/snide/sphinx_rtd_theme/archive/master.tar.gz) and extract the theme
files into `_themes/sphinx_rtd_theme`, i.e. extract the source archive and rename the
`sphinx_rtd_theme-master` directory to `sphinx_rtd_theme`, and move it to the `_theme` directory in
the source tree.

Optionally you can edit `conf.py` to change some settings to fit your needs.

Here comes the last step: if you have a [Make][] program installed, simply run `make html` to
generate the html document in `_build` directory, or run `make latexpdf` if you want to generate the
pdf version. Running `make` will give a list of output formats supported.

## License

Copyright (c) 2015 Hong Xu <hong@topbug.net>

Blowb is a free document: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

Blowb is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License along with Blowb.  If not, see
<http://www.gnu.org/licenses/>.

[git]: http://git-scm.com
[GNU Make]: https://www.gnu.org/software/make/
[Graphviz]: http://www.graphviz.org/
[LaTeX]: http://latex-project.org/ftp.html
[Make]: https://en.wikipedia.org/wiki/Make_(software)
[Sphinx]: http://sphinx-doc.org/
