# django-startproject

Project template for the [Django Web framework][1].

Copyright (c) 2013 Marcus R. Brown and [Contributors](CONTRIBUTORS.md).

The django-startproject project is distributed under the [MIT License](LICENSE.md).

[1]: https://www.djangoproject.com/

## Overview

django-startproject is a Django [project template][2]. You use it to create a
new Django project that includes a bunch of useful functionality
out-of-the-box. The purpose is to consolidate frequently repeated setup and
configuration actions into only a few, and to promote rapid app development.

It is originally based on Randall Degges'
[django-skel](https://github.com/rdegges/django-skel) project, and contains
other features hacked in for use on my own projects and seen in others. I would
like to extend it to support different project types via type-specific
branches.

Contributions, criticisms, and suggestions are [welcome](#author).

[2]: https://docs.djangoproject.com/en/1.5/ref/django-admin/#startproject-projectname-destination

## Getting Started

### Prerequisites

* [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper)

Projects that are created using django-startproject work best within a Python
[virtualenv][3] environment. Run the following commands from a shell to
bootstrap the new project's environment:

    mkvirtualenv myproject
    pip install -r https://raw.github.com/igetgames/django-startproject/master/requirements/development.txt

After the packages have been installed, create the new project with the
following command:

    django-admin.py startproject --template=https://github.com/igetgames/django-startproject/zipball/master -n Procfile myproject

[3]: http://www.virtualenv.org/en/latest/

## Usage

The [django-heroku-fabfile][4] project contains a Fabric fabfile that can be used
for project configuration and maintenance.

TODO: Document available tasks.

[4]: https://github.com/Precision-Mojo/django-heroku-fabfile

## Author

The django-startproject project was created by Marcus R. Brown
([@igetgames](https://twitter.com/#!/igetgames) on Twitter). Send feedback to
mrossbrown@gmail.com.

[![Support via Gittip](https://raw.github.com/igetgames/gittip-badge/master/dist/gittip.png)](https://www.gittip.com/igetgames/)
