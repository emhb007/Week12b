from application import app
from flask import render_template, g
import pymysql
# Section 1 above is used for importing Libraries that we will need.

# Section 2: HELPER FUNCTIONS e.g. DB connection code and methods
def connect_db():
    return pymysql.connect(
        user = 'root', password = 'password', database = 'sakila',
        autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)

def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''
    if hasattr(g, 'db'):
        g.db.close()

# Helper methods
def get_date():
    """ Function to return (fake) date - TASK: Update this - Add the code to pass the current date to the home 	HTML template.
    """
    today = "Today"
    app.logger.info(f"In get_date function! Update so it returns the correct date! {today}")
    return today


# Section 4: APPLICATION ROUTES (WEB PAGE DEFINITIONS)

@app.route('/')
def home():
    """Landing page. Note there is no HTML being written here - it is all kept in the templates/home.html file!
        Data is returned by the query and passed into the template through as the records variable.
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT first_name, last_name, email from Customer")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'home.html',
                title="Using Flask with Templates & MySQL",
                description=f"Python, MySQL, Flask & Jinja. {get_date()}",
                records=result
    )

@app.route('/page1')
def page1():
    """ Second page. Note search param being passed safely. Also result count calculated and passed into description.
    """
    cursor = get_db().cursor()
    cursor.execute("SELECT first_name, last_name FROM actor WHERE last_name=%s ",'Barr')
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'home.html',
                title="Second database query - reusing home template",
                description=f"Another db query. Record count: {len(result)}",
                records=result
    )

@app.route('/page2/<surname>')
def page2(surname):
    """ Third page. Search param searching Customer table
    """
    app.logger.info(surname)
    cursor = get_db().cursor()
    cursor.execute("SELECT first_name, last_name FROM Customer WHERE last_name=%s ",surname)
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'home.html',
                title="Third database query - reusing home template, passing parameter to query",
                description=f"Another db query with parameter from url: surname={surname}.",
                records=result
    )