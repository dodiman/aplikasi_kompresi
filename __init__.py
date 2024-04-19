from flask import Flask
from flask_session import Session

import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    UPLOAD_FOLDER = 'static/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    SESSION_TYPE = 'filesystem'

    pengaturan = {
        'SECRET_KEY': 'dev',
        'UPLOAD_FOLDER': UPLOAD_FOLDER,
        'SESSION_TYPE': SESSION_TYPE
    }

    app.config.from_mapping(pengaturan)

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     # DATABASE=os.path.join(app.instance_path, '')
    # )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import aplikasiku, mulai
    app.register_blueprint(aplikasiku.bp)
    app.register_blueprint(mulai.index.bp)
    
    return app