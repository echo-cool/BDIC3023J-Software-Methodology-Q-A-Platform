import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Students, Permission, Post, Comment, Like, Notification, Transaction, Activity

# if you want to execute the program
# please run this file

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Students=Students, Permission=Permission, Post=Post,
                Comment=Comment, Like=Like, Notification=Notification, Transaction=Transaction, Activity=Activity)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
