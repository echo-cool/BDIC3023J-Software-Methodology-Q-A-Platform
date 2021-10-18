import os
import os
from flask_migrate import Migrate

import app
from app import create_app, db
from app.models import User, Role, Students, Permission, Post, Comment, Like, Notification, Transaction, Activity

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

app.app_context().push()
print(app.config)
print(app.app_context())

print(User.query.all())
print(Role.query.all())
print(Students.query.all())
print(Post.query.all())
print(Comment.query.all())
print(Activity.query.all())