import os, logging, config
from flask_socketio import SocketIO, send, emit

from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask
from models import db, User
from sockets import socketio

logging.basicConfig(
   level=logging.DEBUG,
   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
   datefmt='%Y-%m-%d %H:%M:%S',
   handlers=[logging.StreamHandler()]
)

logger = logging.getLogger()

app_env = config.DevConfig()

app = Flask(__name__)
app.config.from_object(app_env)
mail = Mail(app)
# socketio = SocketIO(app)

if __name__ == '__main__':

    logger.info(f'Starting app in {app_env.ENV_NAME} environment')
    
    db.init_app(app)
    socketio.init_app(app)

    from routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    socketio.run(app, debug=app_env.DEBUG)
