#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#



tasks = [
    {"title": "Task 1", "description": "Description for Task 1"},
    {"title": "Task 2", "description": "Description for Task 2"},
    {"title": "Task 3", "description": "Description for Task 3"},
    {"title": "Task 4", "description": "Description for Task 4"},
    {"title": "Task 5", "description": "Description for Task 5"},
    {"title": "Task 6", "description": "Description for Task 6"},
    {"title": "Task 7", "description": "Description for Task 7"},
    {"title": "Task 8", "description": "Description for Task 8"}
]

upcoming_tasks = [
    {"name": "Task 1", "description": "Description for Task 1"},
    {"name": "Task 2", "description": "Description for Task 2"},
    {"name": "Task 3", "description": "Description for Task 3"}
]

running_tasks = [
    {"id": 1, "name": "Task 1", "description": "Description for Task 1", "addresses": ["Address 1", "Address 2"]},
    {"id": 2, "name": "Task 2", "description": "Description for Task 2", "addresses": ["Address 3", "Address 4"]},
    {"id": 3, "name": "Task 3", "description": "Description for Task 3", "addresses": ["Address 5", "Address 6"]}
]

addresses = ["Address 1", "Address 2", "Address 3", "Address 4", "Address 5", "Address 6", "Address 7", "Address 8"]

user_name = "John Doe"
points = 120  # Example points value

activities = [
    {"name": "Activity 1", "cost": 30, "description": "Description for Activity 1"},
    {"name": "Activity 2", "cost": 50, "description": "Description for Activity 2"},
    {"name": "Activity 3", "cost": 70, "description": "Description for Activity 3"}
]

previous_achievements = ["Achievement 1", "Achievement 2"]
upcoming_achievements = ["Achievement 3"]

@app.route('/')
def home():
    return render_template('pages/home.html', name=user_name, points=points, previous_achievements=previous_achievements, upcoming_achievements=upcoming_achievements, upcoming_tasks=upcoming_tasks)



@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/feladatok')
def feladatok():
    return render_template('pages/feladatok.html')

@app.route('/pontok')
def pontok():
    return render_template('pages/pontok.html', points=points, previous_achievements=previous_achievements, upcoming_achievements=upcoming_achievements, activities=activities)


@app.route('/kopogtatas', methods=['GET', 'POST'])
def kopogtatas():
    selected_addresses = []
    search_query = ""

    if request.method == 'POST':
        if 'task_id' in request.form:
            task_id = int(request.form['task_id'])
            selected_task = next(task for task in running_tasks if task['id'] == task_id)
            selected_addresses = selected_task['addresses']
        elif 'search_query' in request.form:
            search_query = request.form['search_query']
            selected_addresses = [addr for addr in addresses if search_query.lower() in addr.lower()]

    return render_template('pages/kopogtatas.html', tasks=running_tasks, addresses=selected_addresses, search_query=search_query)


@app.route('/telefon')
def telefon():
    return render_template('pages/telefon.html')

@app.route('/szorolap')
def szorolap():
    return render_template('pages/szorolap.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    filtered_tasks = [task for task in tasks if query in task['title'].lower() or query in task['description'].lower()]
    return jsonify(filtered_tasks)





@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
