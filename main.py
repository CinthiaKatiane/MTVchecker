# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smell.core import start
import webbrowser
import sys

if __name__ == '__main__':
    start()
    if ("-w" in sys.argv):
        filename = 'index.html'
        webbrowser.open_new_tab(filename)
