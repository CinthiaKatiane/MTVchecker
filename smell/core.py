# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from smell.checker import checker, counts
from smell.identify import LayerFiles
from smell.converter import SourceToAST
import csv

config = {}

def start():
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

    with open('violations.csv', 'w') as vf:
        wr = csv.writer(vf, quoting=csv.QUOTE_ALL)
        for v in violations:
            if len(v) > 0:
                for i in range(len(v)):
                    wr.writerow([v[i]])
            else:
                pass
    #counts(models, views)

def load_config():
    arquivo = open('config.conf').read().decode("utf8").split('\n')
    for linha in arquivo:
        linha = linha.strip()
        if ':' in linha:
            key, value = linha.split(':')
            config[key] = value
