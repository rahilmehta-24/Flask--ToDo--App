from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s', filename='app.log', filemode='w')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    logging.info('Database created')
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        logging.info('Task created')

        try:
            db.session.add(new_task)
            db.session.commit()
            logging.info('Task added to database')
            return redirect('/')
        except:
            return 'There was an issue adding your task'
            logging.info('Task not added')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        logging.info('Tasks displayed')
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    logging.info('Task deleted')

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        logging.info('Task deleted from database')
        return redirect('/')
        logging.info('redirected to home page')
    except:
        return 'There was a problem deleting that task'
        logging.info('Task not deleted')

@app.route('/update/<int:id>', methods=['GET', 'POST'])


def update(id):
    task = Todo.query.get_or_404(id)


    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            logging.info('Task updated')
            return redirect('/')
            logging.info('redirected to home page')
        except:
            return 'There was an issue updating your task'
            logging.info('Task not updated')

    else:
        return render_template('update.html', task=task)
        logging.info('Task updated')

if __name__ == '__main__':
    app.run(debug=True, port=7777)
    logging.info('App started')