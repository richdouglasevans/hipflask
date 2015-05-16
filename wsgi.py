# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple

from hipflask import create_app

if __name__ == "__main__":
    application = create_app()
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
