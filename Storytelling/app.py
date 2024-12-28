from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Dummy user data for authentication
users = {
    "admin": "password123",  # Replace with your own user data
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are correct
        if username in users and users[username] == password:
            session['username'] = username  # Store the username in the session
            return redirect(url_for('home'))
        else:
            return "Invalid username or password", 401  # Handle invalid login

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists", 400
        users[username] = password
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('home'))

# @app.route('/story/<int:story_id>')
# def story(story_id):
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     story = next((s for s in all_stories if s['id'] == story_id), None)
#     return render_template('story.html', story=story)

@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Handle form submission (e.g., send an email)
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/resources')
def resources():
    if 'username' not in session:
        return redirect(url_for('login'))
    resources_list = [
        {'name': 'Storytelling Resources', 'url': 'https://www.example.com', 'description': 'A collection of storytelling resources.'},
        {'name': 'Creative Writing Tips', 'url': 'https://www.example2.com', 'description': 'Tips and tricks for creative writing.'},
        {'name': 'Literary Community', 'url': 'https://www.example3.com', 'description': 'Join a community of writers and storytellers.'},
        {'name': 'Writing Prompts', 'url': 'https://www.example4.com', 'description': 'Get inspired with writing prompts.'},
        {'name': 'Publishing Resources', 'url': 'https://www.example5.com', 'description': 'Guides on how to publish your work.'},
    ]
    return render_template('resources.html', resources=resources_list)

# # Dummy data for stories
# all_stories = [
#     {"id": 1, "title": "The Adventure Begins", "description": "Join our hero on an exciting journey filled with surprises."},
#     {"id": 2, "title": "A Twist of Fate", "description": "A story about unexpected turns and the magic of destiny."},
#     {"id": 3, "title": "The Lost Treasure", "description": "A thrilling quest to find a treasure hidden for centuries."},
# ]

# featured_stories = [
#     {"id": 1, "title": "The Adventure Begins", "description": "Join our hero on an exciting journey filled with surprises."},
#     {"id":  2, "title": "A Twist of Fate", "description": "A story about unexpected turns and the magic of destiny."},
#     {"id": 3, "title": "The Lost Treasure", "description": "A thrilling quest to find a treasure hidden for centuries."},
# ]

# route for story.html
@app.route('/story')
def story():
    return render_template('story.html')

if __name__ == '__main__':  # Fixed the main block syntax
    app.run(debug=True)