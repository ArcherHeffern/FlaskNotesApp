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
        print(new_task)
        # add to database
        try:
           db.session.add(new_task) 
           db.session.commit()
           return redirect('/')
        except Exception as e:
            return 'There was an issue adding your task ' + str(e)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

    with app.app_context():
        db.create_all()