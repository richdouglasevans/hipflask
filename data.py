# -*- coding: utf-8 -*-

import click
from hipflask import create_app
from hipflask.data import GoldenDataSet


@click.command()
def load_data():
    """
    See the hipflask.data module.
    """

    data_modules = dict(injection_modules=[('hipflask/data', '')])
    app = create_app(settings_override=data_modules)
    injector = app.extensions.get('Injector', None)
    data_set = injector.get(GoldenDataSet)
    data_set.load()


if __name__ == '__main__':
    load_data()
