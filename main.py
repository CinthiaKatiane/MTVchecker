# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smell.core import start
from smellweb.core import begin
import sys
if __name__ == '__main__':
    if ("-w" in sys.argv):
        begin()
    else:
        start()
