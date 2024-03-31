from . import app, db, bcrypt
from flask import render_template, redirect, url_for, session, flash, request
from .models import User, Article
from .forms import SignupForm, LoginForm, ArticleForm
from flask_bcrypt import check_password_hash
from datetime import timedelta


@app.errorhandler(404)  # decorator for handling error#404 whenever it occurs on the website
def error_404(e):
    return 'its error brother'


@app.route('/')  # Decorator to handle requests for the main page
def index():
    """
    Route handler for the main page.

    Returns:
        Renders the main page template with a list of all articles.
    """
    articles = Article.query.all() # Retrieve all articles from the database
    return render_template('main.html', articles=articles) # Render the main page template with the articles


@app.route('/article/<int:article_id>')  # Decorator to handle requests for the article page
def article(article_id):
    """
    Route handler for displaying a specific article.

    Args:
        article_id (int): The ID of the article to display.

    Returns:
        Renders the article page template with the specified article data and its author.
    """
    article_data = Article.query.get(article_id) # Retrieve the article data from the database
    author = User.query.get(article_data.author_id) # Retrieve the author data of the article
    return render_template('article.html', article=article_data, author=author) # Render the article page template with the article data and its author


@app.route('/signup', methods=['GET', 'POST'])  # Decorator to handle GET and POST requests for the signup page
def signup():
    """
    Route handler for the signup page.

    GET:
        Renders the signup form page.

    POST:
        Processes the submitted signup form.
        If the form data is valid:
            - Extracts data from the form.
            - Hashes the password using bcrypt.
            - Creates a new user with the provided data.
            - Commits the new user to the database.
            - Redirects the user to the login page.
        If the form data is not valid:
            - Re-renders the signup form page with validation errors.

    Returns:
        If the request method is GET:
            - Renders the signup form page.
        If the request method is POST and form validation fails:
            - Renders the signup form page with validation errors.
        If the request method is POST and form validation succeeds:
            - Redirects the user to the login page.

    """
    form = SignupForm() # Create an instance of the SignupForm
    if form.validate_on_submit(): # Check if the form has been submitted and is valid
        email = form.email.data # Get the email data from the form
        name = form.name.data # Get the name data from the form
        surname = form.surname.data # Get the surname data from the form
        password = form.password.data # Get the password data from the form

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Hash the password using bcrypt
        new_user = User(email=email, name=name, surname=surname, password=hashed_password) # Create a new User object with the provided data
        db.session.add(new_user) # Add the new user to the database session
        db.session.commit() # Commit the changes to the database

        return redirect(url_for('login')) # Redirect the user to the login page after successful signup

    return render_template('signup.html', form=form) # Render the signup form page with the form object


@app.route('/login', methods=['GET', 'POST'])  # Decorator to handle GET and POST requests for the login page
def login():
    """
    Route handler for the login page.

    GET:
        Renders the login form page.

    POST:
        Processes the submitted login form.
        If the form data is valid:
            - Checks if the user exists in the database and if the password is correct.
            - If authentication is successful, sets the user ID in the session and configures session settings.
            - Redirects the user to their profile page.
        If the form data is not valid:
            - Displays an error message indicating invalid email or password.

    Returns:
        If the request method is GET:
            - Renders the login form page.
        If the request method is POST and form validation fails:
            - Renders the login form page with validation errors.
        If the request method is POST and form validation succeeds but authentication fails:
            - Redirects the user back to the login page with an error message.
        If the request method is POST and authentication succeeds:
            - Redirects the user to their profile page.
    """
    form = LoginForm() # Create an instance of the LoginForm
    if form.validate_on_submit(): # Check if the form has been submitted and is valid
        email = form.email.data # Get the email data from the form
        password = form.password.data # Get the password data from the form

        user = User.query.filter_by(email=email).first() # Retrieve the user from the database by email

        if user and check_password_hash(user.password, password): # Check if user exists and password is correct
            session['user_id'] = user.id # Set user ID in the session
            session.permanent = True # Configure session settings
            app.permanent_session_lifetime = timedelta(days=7)
            return redirect(url_for('profile')) # Redirect the user to their profile page
        else:
            flash('Invalid email or password. Please try again.', 'error') # Display error message for invalid credentials

    return render_template('login.html', form=form) # Render the login form page with the form object


@app.route('/logout')  # Decorator to handle requests for logging out
def logout():
    """
    Route handler for logging out.

    Clears the user ID from the session, effectively logging the user out.

    Returns:
        Redirects the user to the main page after logging out.
    """
    session.pop('user_id', None) # Delete the 'user_id' from the session
    return redirect(url_for('index')) # Redirect the user to the main page


@app.route('/profile')  # Decorator to handle requests for the profile page
def profile():
    """
    Route handler for the profile page.

    If the user is logged in:
        Retrieves the user data from the database using the 'user_id' stored in the session.
        Renders the profile page template with the user data.
    If the user is not logged in:
        Redirects the user to the login page.

    Returns:
        If the user is logged in:
            Renders the profile page template with the user data.
        If the user is not logged in:
            Redirects the user to the login page.
    """
    if 'user_id' in session: # Check if user is logged in
        user = User.query.get(session['user_id']) # Retrieve user data using 'user_id'
        return render_template('dashboard.html', user=user) # Render profile page with user data
    else:
        return redirect(url_for('login')) # Redirect user to login page if not logged in


@app.route('/article_adder', methods=['GET', 'POST'])  # Decorator to handle requests for adding articles
def article_adder():
    """
    Route handler for adding articles.

    GET:
        Renders the page to add a new article.

    POST:
        Processes the submitted form data to add a new article.
        If the user is logged in and the form data is valid:
            - Retrieves the article title and content from the form.
            - Retrieves the current user from the session.
            - Creates a new article associated with the current user.
            - Commits the new article to the database.
            - Redirects the user to the main page.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.

    Returns:
        If the user is logged in and the request method is GET:
            - Renders the page to add a new article with the article form.
        If the user is logged in, the request method is POST, and form validation fails:
            - Renders the page to add a new article with validation errors.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.
    """
    form = ArticleForm() # Create an instance of the ArticleForm
    if 'user_id' in session: # Check if user is logged in
        if form.validate_on_submit(): # Check if form has been submitted and is valid
            title = form.title.data # Get title data from the form
            content = form.content.data # Get content data from the form

            current_user_id = session['user_id'] # Get current user ID from the session
            author = User.query.get(current_user_id) # Retrieve the current user from the database

            new_article = Article(title=title, content=content, author=author) # Create a new article
            db.session.add(new_article) # Add the new article to the database
            db.session.commit() # Commit changes to the database

            return redirect(url_for('index')) # Redirect the user to the main page after adding the article
        return render_template('article_adder.html', form=form) # Render the page to add a new article with the form
    else:
        flash('You need to log in to add an article.', 'error') # Display error message for not logged in users
        return redirect(url_for('login')) # Redirect the user to the login page


@app.route('/add_article', methods=['POST'])  # Decorator for handling requests to add articles
def add_article():
    """
    Function to add articles.

    POST:
        Processes the submitted form data to add a new article.
        If the user is logged in:
            - Retrieves the article title and content from the form.
            - Retrieves the current user from the session.
            - Creates a new article associated with the current user.
            - Commits the new article to the database.
            - Redirects the user to the main page.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.

    Returns:
        If the user is logged in:
            - Redirects the user to the main page after adding the article.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.
    """
    if 'user_id' in session: # Check if user is logged in
        title = request.form['title'] # Get title data from the form
        content = request.form['content'] # Get content data from the form

        current_user_id = session['user_id'] # Get current user ID from the session
        author = User.query.get(current_user_id) # Retrieve the current user from the database

        new_article = Article(title=title, content=content, author=author) # Create a new article
        db.session.add(new_article) # Add the new article to the database
        db.session.commit() # Commit changes to the database

        return redirect(url_for('index')) # Redirect the user to the main page after adding the article
    else:
        flash('You need to log in to add an article.', 'error') # Display error message for not logged in users
        return redirect(url_for('login')) # Redirect the user to the login page


@app.route('/profile/article_editor', methods=['GET', 'POST'])  # Decorator for routing to the article editor page
def article_editor():
    """
    Function for editing articles.

    GET:
        Displays the article editor page if the user is logged in.
        If the user is not logged in, redirects to the login page with an error message.

    POST:
        Processes the submitted form data to edit an article.
        If the user is logged in:
            - Retrieves the article title and content from the form.
            - Creates a new article instance with the provided title and content.
            - Commits the changes to the database.
            - Redirects the user to the main page.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.

    Returns:
        GET:
            If the user is logged in:
                - Renders the article editor page.
            If the user is not logged in:
                - Redirects the user to the login page with an error message.
        POST:
            If the user is logged in:
                - Redirects the user to the main page after editing the article.
            If the user is not logged in:
                - Redirects the user to the login page with an error message.
    """
    if 'user_id' in session: # Check if user is logged in
        if request.method == 'POST': # Check if method is POST
            title = request.form['title'] # Get title data from the form
            content = request.form['content'] # Get content data from the form
            new_article = Article(title=title, content=content) # Create a new article instance
            db.session.add(new_article) # Add the new article to the database
            db.session.commit() # Commit changes to the database
            return redirect(url_for('index')) # Redirect the user to the main page
        return render_template('article_editor.html') # Render the article editor page for GET request
    else:
        flash('You need to log in to access this page.', 'error') # Display error message for not logged in users
        return redirect(url_for('login')) # Redirect the user to the login page


@app.route('/user_articles')  # Decorator for routing to the user articles page
def user_articles():
    """
    Displays the articles authored by the logged-in user.

    If the user is logged in:
        - Retrieves the user's information from the session.
        - Queries the database to get all articles authored by the user.
        - Renders the user_articles.html template with the list of articles.
    If the user is not logged in:
        - Redirects the user to the login page with an error message.

    Returns:
        If the user is logged in:
            - Renders the user_articles.html template.
        If the user is not logged in:
            - Redirects the user to the login page with an error message.
    """
    if 'user_id' in session: # Check if user is logged in
        user = User.query.get(session['user_id']) # Get user information from the session
        articles = Article.query.filter_by(author=user).all() # Get articles authored by the user
        return render_template('user_articles.html', articles=articles) # Render user_articles.html template
    else:
        flash('You need to log in to view your articles.', 'error') # Display error message for not logged in users
        return redirect(url_for('login')) # Redirect the user to the login page


@app.route('/delete_article/<int:article_id>', methods=['POST'])  # Decorator for routing to delete an article
def delete_article(article_id):
    """
    Deletes an article if the user is authorized.

    Args:
        article_id (int): The ID of the article to be deleted.

    Returns:
        Redirects the user to the user_articles page after deleting the article.
    """
    if 'user_id' in session: # Check if user is logged in
        article = Article.query.get(article_id) # Get the article by its ID
        if article.author_id == session['user_id']: # Check if the logged-in user is the author of the article
            db.session.delete(article) # Delete the article from the database
            db.session.commit() # Commit changes
            #flash('Article deleted successfully.', 'success') # Flash message indicating successful deletion (optional)
        else:
            flash('You are not authorized to delete this article.', 'error') # Flash message for unauthorized deletion
    else:
        flash('You need to log in to delete an article.', 'error') # Flash message for not logged in users

    return redirect(url_for('user_articles')) # Redirect the user to the user_articles page


@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])  # Decorator for routing to edit an article
def edit_article(article_id):
    """
    Allows the user to edit an article if authorized.

    Args:
        article_id (int): The ID of the article to be edited.

    Returns:
        Renders the article_editor.html template with the form to edit the article.
    """
    form = ArticleForm() # Create an instance of the ArticleForm class
    if 'user_id' in session: # Check if user is logged in
        article = Article.query.get(article_id) # Get the article by its ID
        if article.author_id == session['user_id']: # Check if the logged-in user is the author of the article
            if form.validate_on_submit(): # Check if the form is submitted and valid
                article.title = form.title.data # Update the article title with form data
                article.content = form.content.data # Update the article content with form data
                db.session.commit() # Commit changes to the database
                #flash('Article updated successfully.', 'success') # Flash message indicating successful update (optional)
                return redirect(url_for('user_articles')) # Redirect the user to the user_articles page after editing
            else:
                form.title.data = article.title # Populate form with existing article title
                form.content.data = article.content # Populate form with existing article content
                return render_template('article_editor.html', form=form, article=article) # Render the article_editor.html template with the populated form and article
        else:
            flash('You are not authorized to edit this article.', 'error') # Flash message for unauthorized editing
            return redirect(url_for('user_articles')) # Redirect the user to the user_articles page
    else:
        flash('You need to log in to edit an article.', 'error') # Flash message for not logged in users
        return redirect(url_for('login')) # Redirect the user to the login page