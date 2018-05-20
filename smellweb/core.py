# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from smellweb.checker import checker
from smellweb.identify import LayerFiles
from smellweb.converter import SourceToAST
import webbrowser
from time import gmtime, strftime

config = {}

def begin():
    load_config()

    identify = LayerFiles(config)
    model_files = identify.get_models()
    view_files = identify.get_views()
    manager_files = identify.load_files('managers')

    converter = SourceToAST(config)
    models = converter.parse(model_files)
    views = converter.parse(view_files)
    managers = converter.parse(manager_files)
    violations = checker(models, views, managers, config)
    Web(violations).create_html()
    #counts(models, views)
class Web():
    def __init__ (self, violations):
        self.v = violations

    def create_html(self):
        outfile = open("smellweb/index.html", "w")
        print >>outfile, """<html>
        <head>
         <title>MTVchecker</title>
         <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                text-align: left;
                padding: 8px;
            }

            tr:nth-child(even){background-color: #f2f2f2}

            th {
                background-color: #4CAF50;
                color: white;
            }
            </style>
        </head>
        <body>
        """
        print >>outfile, "<h1>Relatorio de Code Smells Arquiteturais</h1>"
        print >>outfile, """<table borde="1">
        <tr><th>Modulo</th><th>Quantidade de code smells</th><th>Tipo</th></tr>
        <tr><td>Model</td><td>7</td><td>Meddling Model</td></tr>
        <tr><td>Model</td><td>2</td><td>Fat Repository</td></tr>
        <tr><td>Model</td><td>3</td><td>Laborious Repository Method</td></tr>
        <tr><td>Model</td><td>1</td><td>Brain Repository</td></tr>
        <tr><td>View</td><td>7</td><td>Meddling View</td></tr>
        </table><p>"""


        print >>outfile, """<table borde="1"><tr><th>Smell</th><th>Local</th><th>Linha</th></tr>"""

        for list_violation in self.v:
            for violation in list_violation:
                smell = violation.smell
                local = '{}.{}.{}'.format(violation.module, violation.cls or '-', violation.method or '-')
                line = violation.line
                print >>outfile, '''<tr><td>%s</td><td>%s</td><td>%s</td></tr>''' % (smell, local, line)
        clock = strftime("%d %b %Y", gmtime())
        print >>outfile, """</table>
        <p>Esse relatorio foi gerado em: %s<p>
        </body></html>""" % (clock)

        outfile.close()
        webbrowser.open('smellweb/index.html', new=0, autoraise=True)

def load_config():
    arquivo = open('config.conf').read().decode("utf8").split('\n')
    for linha in arquivo:
        linha = linha.strip()
        if ':' in linha:
            key, value = linha.split(':')
            config[key] = value
