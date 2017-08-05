.. _install:

.. highlight:: bash

Installation
============

How to install
--------------

Installation using conda
^^^^^^^^^^^^^^^^^^^^^^^^
We highly recommend to use conda_ for installing psy-simple. After downloading
the installer from anaconda_, you can install psy-simple simply via::

    $ conda install -c conda-forge psy-simple

.. _anaconda: https://www.continuum.io/downloads
.. _conda: http://conda.io/

Installation using pip
^^^^^^^^^^^^^^^^^^^^^^
If you do not want to use conda for managing your python packages, you can also
use the python package manager ``pip`` and install via::

    $ pip install psy-simple

Running the tests
-----------------
First, clone out the github_ repository. First you have to

- either checkout the reference figures via::

    $ git submodule update --init `python tests/get_ref_dir.py`

- or create the reference figures via::

    $ python setup.py test -a "--ref"

After that, you can run::

    $ python setup.py test

or after having install pytest_::

    $ py.test


.. _pytest: https://pytest.org/latest/contents.html
.. _github: https://github.com/Chilipp/psy-simple
