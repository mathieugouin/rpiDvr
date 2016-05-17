#! /usr/bin/python

###########################################################################
# Bad encoding notes
# https://docs.python.org/2/howto/unicode.html
# http://www.i18nqa.com/debug/utf8-debug.html
# http://www.i18nqa.com/debug/bug-iso8859-1-vs-windows-1252.html
###########################################################################

import re
import io
import sys

def repl(m):
    return unichr(ord(m.group(1)) + 0x40)

for line in sys.stdin:
    # Decode what you receive:
    line = line.decode('utf-8')

    # Fix the problematic chars
    line = re.sub(u'\xc3([\x80-\xbf])', repl, line)

    # Caps A grave
    line = re.sub(u'\xc3\u20ac', u'\xc0', line)

    # Encode what you send:
    line = line.encode('utf-8')
    sys.stdout.write(line)
