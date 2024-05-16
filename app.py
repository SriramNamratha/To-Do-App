from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/",methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title , desc = desc)
        db.session.add(todo)
        db.session.commit()
    all_todos = Todo.query.all()
    return render_template("index.html",all_todos = all_todos)

@app.route("/show")
def products():
     all_todos = Todo.query.all()
     print(all_todos)
     return "this is products page"

@app.route("/delete/<int:sno>")
def delete(sno):
     todo = Todo.query.filter_by(sno=sno).first()
     db.session.delete(todo)
     db.session.commit()
     return redirect("/")

@app.route("/update/<int:sno>")
def update():
     all_todos = Todo.query.all()
     print(all_todos)
     return "this is products page"
if __name__ == "__main__":
    app.run(debug=True)