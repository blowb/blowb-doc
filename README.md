# The Blowb Project

Blowb is a free document project which aims to help individuals and organizations set up servers
which run free/open-source Internet and/or intranet services. The Blowb project also promotes open
[federation](https://en.wikipedia.org/wiki/Federation_(information_technology)) protocols and
software whenever applicable.

The project is currently under development, but you are free to play with it.

Please visit http://docs.blowb.org to read the document.

## Obtain the Latest Source Code

You can always get the latest source code using [git][]:

    git clone --recursive https://gitlab.com/blowb/blowb-doc.git

Or download through [this link](https://gitlab.com/blowb/blowb-doc/repository/archive.tar.gz).

Visit the [project page on GitLab](https://gitlab.com/blowb/blowb-doc) for more details.

## Build the Document

To build the document, first please follow [this link](http://sphinx-doc.org/install.html) to
install [Sphinx][], which is the main tool to build the document. [GNU Make][] or a compatible
[Make][] program is also needed. [Graphviz][] must be installed in order to generate
diagrams. [LaTeX][] is required if you want to generate the PDF version of the document.

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

The contents of this document are licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License][], i.e. CC BY-SA 4.0.

[Creative Commons Attribution-ShareAlike 4.0 International License]: http://creativecommons.org/licenses/by-sa/4.0/
[GNU Make]: https://www.gnu.org/software/make/
[Graphviz]: http://www.graphviz.org/
[LaTeX]: http://latex-project.org/ftp.html
[Make]: https://en.wikipedia.org/wiki/Make_(software)
[Sphinx]: http://sphinx-doc.org/
[git]: http://git-scm.com
