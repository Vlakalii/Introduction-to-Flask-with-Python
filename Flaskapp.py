# the default ip address called loopback ip address refers to this computer
# which is the own machine where the user is working and by convention it means 
# connect to myself. so when visiting the localhost:5000 or http://127.0.0.1:5000
# one is asking the browser to connect to a server that is running
# 5000 is the default port that flask uses and that is just a door through which programs talk
# eg: 80 for HTTP, 443 for HTTPS, 3306 for MySQL
# So 127.0.0.1:5000 just means: “Send traffic to the Flask app running on this computer, through port 5000.”
# to change it one can define the port app.run(host='127.0.0.1', port=8000)
# adding static (css) and templates (html base+ page specific index format)
# this helps us use the render template to run predefined html data files
# for that we imported the render template and url_for which is a flask function
# those were used together with the css and html files
# the html file was defined using base first which is the boiler plate
# then an extension in the index.html which is where one can keep creating different pages
# this html can be called using render_template
# the css file is added into the base.html where the url_for is used but we didnt need to call it or import it




from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# here we are telling our app where the data base is located
# MySQL and Postgres or others can be used here but for simplicity we stick with sqlite
# three forward slashes is a relative path and four are an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# to initialize the data base we will create a model starting with a class
# we set up some columns
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# now we need a function that is gona return a string everytime we create a new element
# so now everytime we make a new element it will return task and the id of the task thats been created

    def __repr__(self):
        return '<Task %r>' % self.id

# after that is done, we need to create and setup our db in the shell
# from app import db -> this imports our db object
# db.create_all() -> this should create our database!




# addition here cuz when deploying on render, an error happens as the db is still not created
with app.app_context():
    db.create_all()



# db.create_all() tells sqlalchemy to look at all the models (classes like todo) that were defined
# and to create the corresponding tables in the data base file defined so test.db if they do not exist
# the todo becomes a real table afterwards
# with app.app_context() is telling flask to pretend like the app is running right now
# so the database operations will work so its basically simulating the app is running
# this is called defining context in flask as flask is strict 
# Flask separates config from execution using something called the Application Context
# Analogy
# Imagine Flask is like a laboratory
# The Flask app is the lab
# The context is when the lab is "open" — lights on, equipment ready
# The database is one of the machines that needs power
# You can't just walk in and press a button — you first have to “open the lab” (start the context)
# then the db is created
# for the route we add some methods as default is just get but to save user input into the database, the post method is needed
# to post into the route and send data to the database
# using request.method means we need to call the request library
# by inserting the if statment and the request method, we differentiate between just showing the page
# which is usig the else which means the request method is a get and the post means there was a user input
# and then itll do just what the user input is defined as
# this is the create part

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # if the request method is post which is a user input
        task_content = request.form['content'] # add the content to a variable and it is requested from the id name content defined in the index html file
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your string'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # query the database is to request information from it
        return render_template('index.html', tasks = tasks)


# here we set up a new route for the delete part
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # here we try to get the task from the database and if it doesnt exist, it is gona 404


    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'



# another route for the update button
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)