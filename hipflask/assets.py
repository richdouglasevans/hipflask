# -*- coding: utf-8 -*-

from flask_assets import Environment, Bundle

from support.strings import prefix_with, has_text


def prepare(app):
    web_assets = Environment(app)

    web_assets.register('css_all', *prepare_css())
    web_assets.register('js_all', *prepare_js())

    is_debugging = app.debug
    web_assets.manifest = 'cache' if not is_debugging else False
    web_assets.cache = not is_debugging
    web_assets.debug = is_debugging

    return app


def prepare_css():
    folder_css = 'css'

    vendor = ('bootstrap.css',
              'bootstrap-theme.css')
    css_vendor = Bundle(*prefix_with(folder_css, vendor),
                        output='{}/vendor.min.css'.format(folder_css))

    custom = ('hipflask.css',)
    css_custom = Bundle(*prefix_with(folder_css, custom),
                        output='{}/hipflask.min.css'.format(folder_css))

    return css_vendor, css_custom


def prepare_js():
    custom = ['angular-lodash.js', 'hipflask.js']
    custom.extend(splat(''))
    js_custom = Bundle(*prefix_with('js', custom))

    vendor = ('vendor.min.js',)
    js_vendor = Bundle(*prefix_with('js/vendor', vendor))

    return js_vendor, js_custom


def splat(module):
    components = []

    if has_text(module):
        component = '{0}/{0}.js'.format(module)
        components.append(component)

        # cater for the singular case of the empty 'root' module
        module = '{}/'.format(module)

    components.extend((
        '{}services/*.js'.format(module),
        '{}filters/*.js'.format(module),
        '{}directives/*.js'.format(module),
        '{}controllers/*.js'.format(module),
        '{}config/*.js'.format(module),
        '{}runs/*.js'.format(module)))

    return components
