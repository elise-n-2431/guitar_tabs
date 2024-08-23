# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, request, Response, render_template, abort

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
  return render_template('main.html',
                          title="My Application")

@app.route("/form")
def form():
  return render_template('form.html',
                          title="Form")
						  
@app.route("/result", methods=['POST'])
def result():
  tabtitle=request.form['tabtitle']
  artist=request.form['artist']
  capo=request.form['capo']
  tab=request.form['tab']
  
  newrecord = (tabtitle,artist,tab,capo)
  with sqlite3.connect("db/Guitar.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO tabs(Title,Artist,Song,Capo) VALUES (?,?,?,?)",newrecord)
        db.commit()

  
  
  return render_template('success.html',
                          title="Form",tabtitle=tabtitle,artist=artist,capo=capo,tab=tab)
 
 
	
	
@app.route("/tabs")
def tabs():
  conn = sqlite3.connect("db/Guitar.db")
  cursor = conn.cursor()
  results = cursor.execute("SELECT * from tabs")
  tabs = [dict(id=row[0], title=row[1], artist=row[2], song=row[3], capo=row[4]) for row in results]
  return render_template('tabs.html',
                          title="Tabs", tabs=tabs)
  cur.execute("SELECT * FROM tabs WHERE title=?", (Variable,))
						  
						  
@app.route("/hey_there_delilah")
def hey_there_delilah():
  return render_template('htd.html',
                          title="Hey There Deliah")
						  
@app.route("/student_edit/<int:id>")
def student_edit(id): # Function definition contains a parameter for ID

## Database Query where ID is selected from a link in the GUI
  conn = sqlite3.connect("db/Guitar.db")
  cursor = conn.cursor()
  query = cursor.execute("SELECT * from tabs WHERE ID={0}".format(id))
  student = cursor.fetchone()
  return render_template('students_edit.html',
                          student=student,
                          id=id)


# This is the function shows the Athletes page
@app.route("/chords")
def chords():

  conn = sqlite3.connect("db/Guitar.db")
  cursor = conn.cursor()
  results = cursor.execute("SELECT * from diningtable")
  chords = [dict(chordname=row[0], string1=row[1], string2=row[2], string3=row[3], string4=row[4], string5=row[5], string6=row[6]) for row in results]

  return render_template('chords.html',
                          title="Chord Chart",chords=chords )
						  
						  



# This function deals with any missing pages and shows the Error page
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
    app.run(debug=True)



