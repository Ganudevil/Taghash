from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Create the database tables
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/progress-tracker')
def progress_tracker():
    return render_template('progress_tracker.html')

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()


    new_task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        due_date=data['dueDate'],
        status=data['status']
    )


    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    # Fetch all tasks from the database
    tasks = Task.query.all()


    tasks_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'dueDate': task.due_date.strftime('%Y-%m-%d'),  # Format date as string
        'status': task.status
    } for task in tasks]

    return jsonify(tasks_list)

if __name__ == '__main__':
    app.run(debug=True)
