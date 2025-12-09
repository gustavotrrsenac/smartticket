from flask import Flask
from models import db

# Blueprints
from routes.chat_ticket_routes import chat_tickets_bp
from routes.usuarios_routes import usuarios_bp
from routes.especialista_routes import especialista_bp
from routes.admin_routes import admin_bp
from routes.fila_especialista_routes import fila_especialista_bp
from routes.home import home_bp

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='static')

    # ==============================
    # Configurações básicas
    # ==============================
    app.config["JSON_SORT_KEYS"] = False

    # ==============================================
    # Registro dos Blueprints
    # ================================================
    app.register_blueprint(chat_tickets_bp, url_prefix="/api")
    app.register_blueprint(usuarios_bp, url_prefix="/api")
    app.register_blueprint(especialista_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(fila_especialista_bp, url_prefix="/api")
    app.register_blueprint(home_bp, url_prefix="/api")

    # ==============================
    # Conexão com banco (Peewee)
    # ==============================
    @app.before_request
    def _db_connect():
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def _db_close(exc):
        if not db.is_closed():
            db.close()

    return app


# ==============================
# Inicialização
# ==============================
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
