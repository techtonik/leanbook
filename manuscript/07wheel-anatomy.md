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

