from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def repr(self):
        return '<Task %r>' % self.id


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_content = request.form["content"]
        new_task = Todo(content = form_content)

        try:
           db.session.add(new_task) 
           db.session.commit()
           return redirect('/')
        except Exception as e:
            return 'There was an issue adding your task ' + str(e)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
        
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        task = Todo.query.get_or_404(id)
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return e
        

        try:
            return 'something good happened'
        except Exception as e:
            return 'Error: ' + str(e)

    else:
        return render_template('update.html', id=id)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return 'Error: ' + str(e)

if __name__ == "__main__":
    app.run(debug=True)

    with app.app_context():
        db.create_all()