from myproject import app, db
from myproject.models import User, Post

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}