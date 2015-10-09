# Anatomy of a wheel

**Python wheel** is a .zip file that promises to contain all files
"in a way that is very close to the on-disk format".

The structure of a wheel archive is described at 
https://www.python.org/dev/peps/pep-0427/#installing-a-wheel-distribution-1-0-py32-none-any-whl

But it is not clear enough. In summary, the obligatory contents of a wheel:

    distribution-1.0.dist-info/    - package description directory
      METADATA                     - package content description
      RECORD                       - file list
      WHEEL                        - additional package description

Creating .whl without METADATA gives a fatal error while installing with
pip 7.1.2. With empty METADATA it exits with message `distribution is in
an unsupported or invalid wheel`. So METADATA alone is not enough, you
need to create additional file WHEEL where pip expects to find at least:

    Wheel-Version: 0.1

But that is not enough either. The RECORD file is obligatory as well. So
an archive named something-0.5.0-py2-none-any.whl with empty METADATA and
RECORD and a single line WHEEL file is a valid **wheel** file that can be
successfully installed and uninstalled with **pip**.

Strange that package requires both METADATA and WHEEL to describe it. One
of those files should perish, as for me. Looks like METADATA is not
extensive enough to include extra fields. From the other side all its info
could be present in a WHEEL file. Anyway.. Let's see if that wheel will be
accepted by PyPI.

### Uploading wheel to PyPI

First, PyPI can't just take .whl, parse it and merge metadata from there.
That's a pity. So you will need to create package `something` manually by
submitting the form with required fields online. After that you can upload
that crippled wheel without any problem.

### Adding contents

Handling empty wheels is so much fun, but let's make it better. Just add
some files into .whl and they will get magically unpacked into Python's
`site-packages`	directory on installing. That's it.

Clearly the best packaging format.

### Platform specific code 

Sometimes you need to ship compiled C extensions. These come as DLLs in
Windows or SO files in Linux. Both can be 32 or 64 bits. For that, wheels
require to specify target platform in filename.

    somethings-1.0.1-py2-none-win32.whl
          ^^^^                          - name
                ^^^^                    - version
                     ^^^                - Python version (can be py2.py3)
                         ^^^^           - mystic ABI
                               ^^^^     - platform

The ABI is relevant to C extension writers. Platform can be `win32`,
`linux_i386` and `linux_x86_64`.

So compile your stuff, create yourstuff-version.dist-info/ directory with
three files, and add stuff to the root of the archive. Name it
appropriately for your platform / Python version and you're all set. No
need for complicated `setup.py` dances.

### Bonus

For the test, I added `emptywheel-1.0.1-py2-none-any.whl` to the data/
directory in the source code of this book. Try to install it and locate
`find me` in your `site-packages`.

I also include `testdata-wheel-reversing.zip` with the wheels I used to
test `pip` behaviour. 

And for the last thing, I include `create-record.py` script that can be
used to create RECORD from an existing directory heirarchy. It is useless
for the time being, but may become handy in future if `pip` gets more
strict checks for unpacking the wheels.
