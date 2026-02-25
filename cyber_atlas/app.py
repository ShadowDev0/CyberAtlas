from flask import Flask
from extensions import db, login_manager
from models import User

def create_app():
    app = Flask(__name__)
    # Clé secrète pour sécuriser les sessions et les mots de passe
    app.config['SECRET_KEY'] = 'une_cle_secrete_tres_difficile_a_deviner'
    # Fichier de base de données qui sera créé automatiquement
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberatlas.db'
    
    # On relie les extensions à notre application
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Permet à Flask-Login de retrouver un utilisateur grâce à son ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # On importe et on enregistre nos Blueprints (modules)
    from routes.auth import auth_bp
    from routes.api import api_bp
    from routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)

    # Crée les tables dans la base de données si elles n'existent pas encore
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)