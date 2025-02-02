from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Job Hunter API",
            "description": "API to get relevant data regarding a technology.",
            "version": "1.0.0",
        },
        "host": "localhost:5001",
        "basePath": "/",
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    from app.routes.wiki_link_routes import wiki_link_bp
    app.register_blueprint(wiki_link_bp)
    return app
