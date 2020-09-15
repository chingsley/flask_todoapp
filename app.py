from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kingsleyeneja:chinonxo@localhost:5432/flask_todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed  = db.Column(db.Boolean, nullable=False, default=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'


# db.create_all()


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  response_body = {}
  try:
    # description = request.form.get('description', '')
    description = request.get_json()['description']
    todo  = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    response_body = { 'description': todo.description}
    # return redirect(url_for('index')) # the 'index' here refers to the controller method (def index) defined below. It doesn't not refer to the index.html file
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    return jsonify(response_body)




@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())