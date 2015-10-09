# So, what is a source package?

In terminology chapter two primary things were described:

  * importable Python package - a directory with __init__.py
  * archive with Python source or compiled extensions

Python 2.7.9 docs are also distinct about **pure Python package** or
**source package** and **binary distribution**. This is clearly inspired
by Linux where you have this distinction - software in source form and
software in compiled form all need to be packed for distribution.

There is somewhat vague definition of **source package** as archive
produced by `setup.py sdist`. A more appropriate definition is that
**source package is** a .tar.gz or .zip file with subdirectory named
after the archive and `setup.py` inside of it. It is not clear why this
extra directory is necessary, becuase `pip` is able to install archive
even without it.

