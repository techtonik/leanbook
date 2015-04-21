What a **Python source package**?

An informal official definition:

  Python source package is an archive in OS system specific
  archive format (.tar.gz or .zip) produced by
  **setup.py sdist** command.

That definition is not sufficient to understand what
exactly the package contains and how it can be used. The
only thing that is evident is that nothing except `sdist'
command can produce such package.

A more useful non-official definition could be:

  Packed Python sources that can be installed on target
  system and/or compiled into binary package format.

Or alternative:

  Archive with packed pure Python code that can be
  installed by pip from PyPI.

So if the can be installed and contains the full source of
the Python application/module, that is a **source
package** (if it looks like a duck and quacks like a duck,
then it is a duck).


### Reversing the Python source distribution format

But what is in the archive exactly? I took the existing
package named hexdump-3.2.zip and tried to modify it to
see what is possible and what is not. It appeared that the
following could be uploaded to PyPI and installed using
pip. This test was done with pip 1.5.4 in April 2015. I
mention this, because thing may break in future if PyPA
team decides to "fix the issue".

 * [x] .zip with setup.py at root (hexdump-3.2.zip)
 * [x] .zip with setup.py at root (renamed to blabla.zip)
 * [x] .zip with setup.py in arbitrary directory inside
       of archive (must contain exactly one directory at
       root level and nothing else)

So, the setup.py file looks important, let's see how it
works without learning any Python code at all. That's the
point of whole point of reversing - learning stuff in non
standard ways is fun.


### Researching setup.py behaviour

Removing setup.py from archive and trying to install this
.zip produces an error.

    $ pip install blabla.zip
    Processing c:\leanbook\manuscript\blabla.zip
        Complete output from command python setup.py egg_info:
        Traceback (most recent call last):
          File "<string>", line 18, in <module>
          File "C:\Python34\lib\tokenize.py", line 437, in open
            buffer = builtins.open(filename, 'rb')
        FileNotFoundError: [Errno 2] No such file or directory:
    'C:\\Temp\\pip-7rc60spl-build\\setup.py'

        ----------------------------------------
        Command "python setup.py egg_info" failed with error code 1
    in C:\Temp\pip-7rc60spl-build

This time I upgraded pip to 6.1.1 (latest released
version as of April 2015).

`pip` is trying to execute it with `egg_info` command.
This is strange, because setup.py is described in official
Python docs, but there is no `egg_info`, so it must be
some internal `pip` hack.

Let's create an empty *setup.py* to see how it behaves:

    $ pip install blabla.zip
    No files/directories in C:\Temp\pip-82yc9aep-build\pip-egg-info
    (from PKG-INFO)

This is completely mystic, but gives a hint aboout some
PKG-INFO. Looking into former hexdump-3.2.zip before
modification, there is a PKG-INFO file with a lot of content.
Placing empty PKG-INFO together with empty setup.py gives
the same error as above. Actually, the PKG-INFO doesn't
matter at all - even complete file still gives the
misleading error.

So, getting back to the setup.py, after some experiments,
this is the minimal magic incantation to write into setup.py
to get something installed:

    from distutils.core import setup
    setup(
        py_modules=['hexdump'],
    )

With such file pip will install hexdump as UNKNOWN-0.0.0
package. The optimal content looks like this:

    from distutils.core import setup

    setup(
        name='hexdump',
        version='3.2',
        author='anatoly techtonik <techtonik@gmail.com>',
        url='https://bitbucket.org/techtonik/hexdump/',

        description="view/edit your binary with any text editor",
        license="Public Domain",

        py_modules=['hexdump'],
    )

This is weird. Even after so many years of dealing with that
file I still look at it as to awkward and non-intuitive way
to package or build stuff. But there is no alternative to
setup.py from what I know.
