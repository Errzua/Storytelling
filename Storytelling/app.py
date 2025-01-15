from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Default XAMPP username
        password="",  # Default XAMPP password
        database="storytelling"
    )

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

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                if user and check_password_hash(user[0], password):  # Validate hashed password
                    session['username'] = username
                    return redirect(url_for('home'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()

        return "Invalid username or password", 401  # Handle invalid login

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        contact_no = request.form['contact_no']
        age = request.form['age']
        grade_level = request.form['grade_level']

        if password != confirm_password:
            return "Passwords do not match", 400

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Check if the username already exists
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    return "Username already exists", 400

                # Hash the password before saving it
                hashed_password = generate_password_hash(password)

                # Insert the new user into the database
                cursor.execute("""
                    INSERT INTO users (username, password, address, contact_no, age, grade_level)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, hashed_password, address, contact_no, age, grade_level))
                connection.commit()  # Commit the changes

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred", 500  # Handle any errors
        finally:
            connection.close()  # Ensure the connection is closed

        return redirect(url_for('login'))

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

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, address, contact_no, age, grade_level FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                return render_template('profile.html', user=user)
            else:
                return "User  not found", 404
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred", 500
    finally:
        connection.close()

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
