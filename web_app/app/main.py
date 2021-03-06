"""
set up apps and register the blue print.
"""

from flask import Flask
from database import db_session, init_db
from views.blueviews import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['SECRET_KEY'] = 'iwalkinthev@11yoftheShadowofdeath'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# clean up time!!
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.before_first_request
def init_app():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

