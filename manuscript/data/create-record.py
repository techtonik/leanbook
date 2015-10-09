"""
Create RECORD file for .whl

License: CC0/Public Domain
Author: anatoly techtonik <techtonik@gmail.com>

"""

import fnmatch
import hashlib
import os
import sys

if '-h' in sys.argv:
  sys.exit('usage: create-record.py [dir]')

if sys.argv[1:]:
  startfrom = sys.argv[1]
else:
  startfrom = '.'

matches = []
for root, dirnames, filenames in os.walk(startfrom):
  for filename in filenames:
    relpath = os.path.join(root, filename).replace('\\', '/').lstrip('./')
    sha1hash = hashlib.sha1(open(relpath, 'rb').read()).hexdigest()
    filesize = os.path.getsize(relpath)
    print os.path.join(relpath) + ',' + sha1hash + ',' + str(filesize)

