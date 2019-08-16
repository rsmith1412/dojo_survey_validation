from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "something so secret"
# our index route will handle rendering our form
@app.route('/')
def index():
    mysql = connectToMySQL('dojo_survey_validation')
    locations = mysql.query_db("SELECT * FROM locations;")
    mysql = connectToMySQL('dojo_survey_validation')
    languages = mysql.query_db("SELECT * FROM languages;")
    return render_template("index.html", locations = locations, languages = languages)

@app.route('/submission', methods=['POST'])
def submit_info():
    print("Got Post Info")
    print(request.form)
    is_valid = True;
    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Please enter a first name")
    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("Please enter a last name")
    if len(request.form['comment']) > 120:
        print(len(request.form['comment']))
        is_valid = False
        flash("Comments should not exceed 120 characters")
    
    if is_valid:
        mysql = connectToMySQL('dojo_survey_validation')	        # call the function, passing in the name of our db
        query = "INSERT INTO users (first_name, last_name, comment, gender, language_id, location_id, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(com)s, %(gen)s, %(lang)s, %(loc)s, NOW(), NOW());"
        data = {
            "fn": request.form["first_name"],
            "ln": request.form["last_name"],
            "gen": request.form["gender"],
            "loc": request.form["location"],
            "lang": request.form["language"],
            "com": request.form["comment"]
        }
        session["id"] =  mysql.query_db(query, data)
        return redirect("/result")
    return redirect('/')

@app.route('/result')
def display_submission():
    print("Got Session Info")
    print(session["id"])
    mysql = connectToMySQL('dojo_survey_validation')	        # call the function, passing in the name of our db
    query = "SELECT * FROM users JOIN locations ON users.location_id = locations.id JOIN languages ON users.language_id = languages.id WHERE users.id = %(id)s;"
    data = {
        "id": session["id"]
    }
    display_user = mysql.query_db(query, data)
    flash("Thank you for your feedback!")
    print("???????", display_user)
    return render_template('results.html', display_this_user = display_user[0])

if __name__ == "__main__":
    app.run(debug=True)