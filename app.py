from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import uuid 
import markdown 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Glitch_C0r' 


users = {} 
teams = {} 
projects = [] 
tasks = []


PROJECT_PROGRESS_OPTIONS = [
    "Not Started",
    "Planning",
    "In Progress",
    "Testing",
    "Completed",
    "On Hold",
    "Cancelled"
]


def generate_id():
    return str(uuid.uuid4())


def _initialize_test_data():
    """
    Initializes some test users and teams for easier debugging.
    This data is in-memory and will be lost on server restart.
    """
    print("Initializing test data...")
    # Add a test user
    if 'testuser' not in users:
        user_id = generate_id()
        users['testuser'] = {
            'id': user_id,
            'username': 'testuser',
            'password_hash': generate_password_hash('password')
        }
        print(f"Added testuser: {users['testuser']}")
    
    
    if 'anotheruser' not in users:
        user_id_2 = generate_id()
        users['anotheruser'] = {
            'id': user_id_2,
            'username': 'anotheruser',
            'password_hash': generate_password_hash('password')
        }
        print(f"Added anotheruser: {users['anotheruser']}")


    
    test_team_id = 'test_team_123' 
    if test_team_id not in teams:
        teams[test_team_id] = {
            'id': test_team_id,
            'name': 'Alpha Team',
            'member_ids': [users['testuser']['id']]
        }
        print(f"Added Alpha Team: {teams[test_team_id]}")
        print(f"Testuser is a member of Alpha Team (ID: {test_team_id})")
    elif users['testuser']['id'] not in teams[test_team_id]['member_ids']:
        teams[test_team_id]['member_ids'].append(users['testuser']['id'])
        print(f"Ensured testuser is a member of Alpha Team (ID: {test_team_id})")
    
    
    if users['anotheruser']['id'] not in teams[test_team_id]['member_ids']:
        teams[test_team_id]['member_ids'].append(users['anotheruser']['id'])
        print(f"Ensured anotheruser is a member of Alpha Team (ID: {test_team_id})")



    test_team_id_2 = 'test_team_456'
    if test_team_id_2 not in teams:
        teams[test_team_id_2] = {
            'id': test_team_id_2,
            'name': 'Beta Squad',
            'member_ids': []
        }
        print(f"Added Beta Squad: {teams[test_team_id_2]}")


@app.before_request
def load_logged_in_user():
    """Load the logged-in user's data into Flask's global 'g' object."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
       
        g.user = next((u for u in users.values() if u['id'] == user_id), None)

@app.errorhandler(404)
def page_not_found(e):
    """Handles 404 Not Found errors."""
    return render_template('404.html'), 404



@app.route('/')
def root():
    """Redirects to landing page if not logged in, or projects dashboard if logged in."""
    if g.user:
        return redirect(url_for('projects_dashboard'))
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    """Renders the landing page."""
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user registration."""
    if g.user: 
        return redirect(url_for('projects_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif username in users:
            error = f'User {username} is already registered.'

        if error is None:
            user_id = generate_id()
            users[username] = {
                'id': user_id,
                'username': username,
                'password_hash': generate_password_hash(password)
            }
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        flash(error, 'error')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if g.user: 
        return redirect(url_for('projects_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user_data = users.get(username)

        if user_data is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user_data['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user_data['id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('projects_dashboard'))
        
        flash(error, 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs out the current user."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('landing'))



def login_required(view):
    """Decorator to protect routes, ensuring a user is logged in."""
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view



@app.route('/teams')
@login_required
def teams_dashboard():
    """Renders the dashboard showing teams the user is a member of."""
    user_teams = [team for team_id, team in teams.items() if g.user['id'] in team['member_ids']]
    return render_template('teams_dashboard.html', user_teams=user_teams)

@app.route('/team/add', methods=['GET', 'POST'])
@login_required
def add_team():
    """Handles adding a new team."""
    if request.method == 'POST':
        team_name = request.form['name']
        error = None
        if not team_name:
            error = 'Team name is required.'
        
       
        if any(team['name'] == team_name for team in teams.values()):
            error = 'A team with this name already exists.'

        if error is None:
            team_id = generate_id()
            teams[team_id] = {
                'id': team_id,
                'name': team_name,
                'member_ids': [g.user['id']] 
            }
            flash(f'Team "{team_name}" created successfully!', 'success')
            return redirect(url_for('teams_dashboard'))
        
        flash(error, 'error')
    return render_template('add_team.html')

@app.route('/team/join', methods=['GET', 'POST'])
@login_required
def join_team():
    """Allows a user to join an existing team by ID."""
    if request.method == 'POST':
        team_id_to_join = request.form['team_id']
        team = teams.get(team_id_to_join)
        error = None

        if not team:
            error = 'Team not found with that ID.'
        elif g.user['id'] in team['member_ids']:
            error = 'You are already a member of this team.'
        
        if error is None:
            team['member_ids'].append(g.user['id'])
            flash(f'Successfully joined team "{team["name"]}"!', 'success')
            return redirect(url_for('teams_dashboard'))
        
        flash(error, 'error')
    return render_template('join_team.html')

@app.route('/team/<team_id>/leave', methods=['POST'])
@login_required
def leave_team(team_id):
    """Allows a user to leave a team."""
    team = teams.get(team_id)
    if not team:
        flash('Team not found!', 'error')
        return redirect(url_for('teams_dashboard'))
    
    if g.user['id'] in team['member_ids']:
        team['member_ids'].remove(g.user['id'])
        flash(f'You have left team "{team["name"]}".', 'info')
        
        if not team['member_ids']:
            del teams[team_id]
           
            global projects, tasks
            projects = [p for p in projects if p.get('team_id') != team_id]
            tasks = [t for t in tasks if t.get('team_id') != team_id] # Tasks inherit team_id from project
            flash(f'Team "{team["name"]}" was disbanded as it had no members left.', 'info')
    else:
        flash('You are not a member of this team.', 'error')
    
    return redirect(url_for('teams_dashboard'))



@app.route('/projects')
@login_required
def projects_dashboard():
    """Renders the main dashboard showing all projects for the logged-in user."""
   
    owned_projects = [p for p in projects if p.get('owner_id') == g.user['id']]

    
    user_team_ids = {team_id for team_id, team in teams.items() if g.user['id'] in team['member_ids']}
    team_projects = [p for p in projects if p.get('team_id') in user_team_ids]

    
    all_user_accessible_projects = {}
    for p in owned_projects + team_projects:
        all_user_accessible_projects[p['id']] = p
    
    final_projects = list(all_user_accessible_projects.values())


    for project in final_projects:
        team_id = project.get('team_id')
        if team_id:
            team = teams.get(team_id)
            project['team_name'] = team['name'] if team else 'Unknown Team'
        else:
            project['team_name'] = 'No Team'

    return render_template('index.html', projects=final_projects)

@app.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """Handles adding a new project. Team selection is now optional, and progress is added."""
   
    user_teams = [team for team_id, team in teams.items() if g.user['id'] in team['member_ids']]

    if request.method == 'POST':
        project_name = request.form.get('name')
        project_description = request.form.get('description')
        selected_team_id = request.form.get('team_id') 
        project_progress = request.form.get('progress') 

        error = None
        if not project_name:
            error = 'Project name is required.'
        if not project_progress or project_progress not in PROJECT_PROGRESS_OPTIONS:
            error = 'Invalid project progress selected.'
        
        
        if selected_team_id:
            team_exists_and_user_is_member = any(t['id'] == selected_team_id for t in user_teams)
            if not team_exists_and_user_is_member:
                error = 'Invalid team selected or you are not a member of that team.'

        if error:
            flash(error, 'error')
            return render_template('add_project.html', user_teams=user_teams, PROJECT_PROGRESS_OPTIONS=PROJECT_PROGRESS_OPTIONS)

        new_project = {
            'id': generate_id(),
            'name': project_name,
            'description': project_description,
            'created_at': 'Today', 
            'tasks_count': 0, 
            'team_id': selected_team_id if selected_team_id else None, 
            'owner_id': g.user['id'], 
            'progress': project_progress 
        }
        projects.append(new_project)
        
        team_msg = f' to team "{teams[selected_team_id]["name"]}"' if selected_team_id else ''
        flash(f'Project "{project_name}" added successfully{team_msg}!', 'success')
        return redirect(url_for('projects_dashboard'))
    
    return render_template('add_project.html', user_teams=user_teams, PROJECT_PROGRESS_OPTIONS=PROJECT_PROGRESS_OPTIONS)

@app.route('/project/<project_id>')
@login_required
def project_detail(project_id):
    """Renders the detail page for a specific project, checking access based on ownership or team membership."""
    project = next((p for p in projects if p['id'] == project_id), None)
    
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('projects_dashboard'))
    

    has_access = False
    if project.get('owner_id') == g.user['id']:
        has_access = True
    elif project.get('team_id'):
        project_team = teams.get(project['team_id'])
        if project_team and g.user['id'] in project_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to this project.', 'error')
        return redirect(url_for('projects_dashboard'))

    project_tasks = [t for t in tasks if t['project_id'] == project_id] 

    
    project['tasks_count'] = len(project_tasks)

 
    project_description_html = markdown.markdown(project['description'])


    team_info = None
    team_members_data = []
    if project.get('team_id'):
        project_team = teams.get(project['team_id'])
        if project_team:
            team_info = project_team
        
            for member_id in project_team['member_ids']:
                # Find the user object by ID
                member_user = next((u for u in users.values() if u['id'] == member_id), None)
                if member_user:
                    team_members_data.append(member_user['username'])
    
    return render_template('project_detail.html', 
                           project=project, 
                           tasks=project_tasks,
                           project_description_html=project_description_html,
                           team_info=team_info, 
                           team_members_data=team_members_data) 

@app.route('/project/<project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Handles editing an existing project, checking access based on ownership or team membership."""
    project = next((p for p in projects if p['id'] == project_id), None)
    
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('projects_dashboard'))

    has_access = False
    if project.get('owner_id') == g.user['id']:
        has_access = True
    elif project.get('team_id'):
        project_team = teams.get(project['team_id'])
        if project_team and g.user['id'] in project_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to edit this project.', 'error')
        return redirect(url_for('projects_dashboard'))

    user_teams = [team for team_id, team in teams.items() if g.user['id'] in team['member_ids']]

    if request.method == 'POST':
        project_name = request.form.get('name')
        project_description = request.form.get('description')
        new_team_id = request.form.get('team_id')
        project_progress = request.form.get('progress') 

        error = None
        if not project_name:
            error = 'Project name is required.'
        if not project_progress or project_progress not in PROJECT_PROGRESS_OPTIONS:
            error = 'Invalid project progress selected.'
        
    
        if new_team_id:
            team_exists_and_user_is_member = any(t['id'] == new_team_id for t in user_teams)
            if not team_exists_and_user_is_member:
                error = 'Invalid team selected or you are not a member of that team.'
        
        if error:
            flash(error, 'error')
            return render_template('edit_project.html', project=project, user_teams=user_teams, PROJECT_PROGRESS_OPTIONS=PROJECT_PROGRESS_OPTIONS)

        project['name'] = project_name
        project['description'] = project_description
        project['team_id'] = new_team_id if new_team_id else None 
        project['progress'] = project_progress 

        flash(f'Project "{project["name"]}" updated successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('edit_project.html', project=project, user_teams=user_teams, PROJECT_PROGRESS_OPTIONS=PROJECT_PROGRESS_OPTIONS)

@app.route('/project/<project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Handles deleting a project and its associated tasks, checking access based on ownership or team membership."""
    global projects, tasks
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('projects_dashboard'))
    

    has_access = False
    if project.get('owner_id') == g.user['id']:
        has_access = True
    elif project.get('team_id'):
        project_team = teams.get(project['team_id'])
        if project_team and g.user['id'] in project_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to delete this project.', 'error')
        return redirect(url_for('projects_dashboard'))
    

    projects = [p for p in projects if p['id'] != project_id]
 
    tasks = [t for t in tasks if t['project_id'] != project_id]
    
    flash(f'Project "{project["name"]}" and its tasks deleted successfully!', 'success')
    return redirect(url_for('projects_dashboard'))

@app.route('/project/<project_id>/task/add', methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    """Handles adding a new task to a specific project, checking access based on ownership or team membership."""
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('projects_dashboard'))


    has_access = False
    if project.get('owner_id') == g.user['id']:
        has_access = True
    elif project.get('team_id'):
        project_team = teams.get(project['team_id'])
        if project_team and g.user['id'] in project_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to add tasks to this project.', 'error')
        return redirect(url_for('projects_dashboard'))

    if request.method == 'POST':
        task_name = request.form.get('name')
        task_description = request.form.get('description')
        task_due_date = request.form.get('due_date')
        task_status = request.form.get('status')

        error = None
        if not task_name:
            error = 'Task name is required.'
        if error:
            flash(error, 'error')
            return render_template('add_task.html', project=project)

        new_task = {
            'id': generate_id(),
            'project_id': project_id,
            'name': task_name,
            'description': task_description,
            'due_date': task_due_date,
            'status': task_status,
            'completed': False,
            'owner_id': g.user['id'], 
            'team_id': project.get('team_id')
        }
        tasks.append(new_task)
        flash(f'Task "{task_name}" added to "{project["name"]}" successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('add_task.html', project=project)

@app.route('/project/<project_id>/task/<task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(project_id, task_id):
    """Handles editing an existing task, checking access based on ownership or team membership."""
    task = next((t for t in tasks if t['id'] == task_id and t['project_id'] == project_id), None)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('project_detail', project_id=project_id))


    has_access = False
    if task.get('owner_id') == g.user['id']:
        has_access = True
    elif task.get('team_id'):
        task_team = teams.get(task['team_id'])
        if task_team and g.user['id'] in task_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to edit this task.', 'error')
        return redirect(url_for('project_detail', project_id=project_id))

    if request.method == 'POST':
        task_name = request.form.get('name')
        task_description = request.form.get('description')
        task_due_date = request.form.get('due_date')
        task_status = request.form.get('status')
        task_completed = 'completed' in request.form

        error = None
        if not task_name:
            error = 'Task name is required.'
        if error:
            flash(error, 'error')
            return render_template('edit_task.html', project_id=project_id, task=task)

        task['name'] = task_name
        task['description'] = task_description
        task['due_date'] = task_due_date
        task['status'] = task_status
        task['completed'] = task_completed
        flash(f'Task "{task["name"]}" updated successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('edit_task.html', project_id=project_id, task=task)

@app.route('/project/<project_id>/task/<task_id>/toggle', methods=['POST'])
@login_required
def toggle_task_completion(project_id, task_id):
    """Toggles the completion status of a task, checking access based on ownership or team membership."""
    task = next((t for t in tasks if t['id'] == task_id and t['project_id'] == project_id), None)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('project_detail', project_id=project_id))

    has_access = False
    if task.get('owner_id') == g.user['id']:
        has_access = True
    elif task.get('team_id'):
        task_team = teams.get(task['team_id'])
        if task_team and g.user['id'] in task_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to modify this task.', 'error')
        return redirect(url_for('project_detail', project_id=project_id))

    task['completed'] = not task['completed']
    flash(f'Task "{task["name"]}" completion status updated!', 'info')
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/project/<project_id>/task/<task_id>/delete', methods=['POST'])
@login_required
def delete_task(project_id, task_id):
    """Handles deleting a task from a project, checking access based on ownership or team membership."""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id and t['project_id'] == project_id), None)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('project_detail', project_id=project_id))
    
    has_access = False
    if task.get('owner_id') == g.user['id']:
        has_access = True
    elif task.get('team_id'):
        task_team = teams.get(task['team_id'])
        if task_team and g.user['id'] in task_team['member_ids']:
            has_access = True
    
    if not has_access:
        flash('You do not have access to delete this task.', 'error')
        return redirect(url_for('project_detail', project_id=project_id))

    tasks = [t for t in tasks if not (t['id'] == task_id and t['project_id'] == project_id)]
    flash(f'Task "{task["name"]}" deleted successfully!', 'success')
    return redirect(url_for('project_detail', project_id=project_id))


if __name__ == '__main__':
    _initialize_test_data()
    app.run(debug=True)
