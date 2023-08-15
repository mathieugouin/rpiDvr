#! /usr/bin/python

###########################################################################
# Bad encoding notes
# https://docs.python.org/2/howto/unicode.html
# http://www.i18nqa.com/debug/utf8-debug.html
# http://www.i18nqa.com/debug/bug-iso8859-1-vs-windows-1252.html
###########################################################################

import re
import sys


for line in sys.stdin:
    # Decode what you receive:
    line = line.decode('utf-8')

    # Check problematic chars
    if re.search(u'\xc3([\x80-\xff])', line):
        # Encode what you send:
        line = line.encode('utf-8')
        sys.stdout.write(line)
