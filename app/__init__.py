from flask import Flask, redirect, url_for

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registra os controllers (Blueprints)
    from app.controllers.auth import auth_bp
    from app.controllers.produto_controller import produto_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)

    @app.route("/")
    def index():
        return redirect(url_for("produtos.listar"))

    # Cria as tabelas no PostgreSQL caso ainda não existam
    with app.app_context():
        from app.models import produto, usuarios  # noqa: F401

        db.create_all()

    return app
