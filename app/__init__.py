from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.routes.wiki_link_routes import wiki_link_bp
    app.register_blueprint(wiki_link_bp)
    return app
