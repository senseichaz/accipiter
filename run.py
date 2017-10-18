# run.py

from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename
import os
import subprocess
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set SQLAlchemy settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pclouds.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define path for file uploads
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class pcloud(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pagename = db.Column(db.String(128))

    def __init__(self, pagename):
        self.pagename = pagename

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index.html')
def index2():
    return render_template("index.html")

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/sampler.html')
def sampler():
    return render_template("sampler.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/howitworks.html')
def howitworks():
    return render_template("howitworks.html")

@app.route('/upload.html')
def uplo():
    return render_template("upload.html")

@app.route('/<pagename>')
def cloud_viewer(pagename):
    return render_template("/converted/" + pagename)

@app.route('/viewall')
def viewall():
    print pcloud.query.filter_by(pagename='stadium-utm').first().id

    return '1'

@app.route('/potest')
def cloud_generate(filename):

      pagename = filename[0:(len(filename)-4)]

      file_path_string = '~/dev/accipiter/uploads/' + filename
      file_output_string = '~/dev/accipiter/templates/converted'
      call_string = 'PotreeConverter -i ' + file_path_string + ' -o ' + file_output_string + ' -p ' + pagename

      subprocess.call(call_string, shell=True)

      # change html line for proper pointclouds directory
      call_string_htmledit = "sed -i 's/pointclouds/static\/pointclouds/g' " + file_output_string + "/" + pagename + ".html"
      subprocess.call(call_string_htmledit, shell=True)

      # move pointcloud to static directory
      subprocess.call("mv ~/dev/accipiter/templates/converted/pointclouds/" + pagename + " ~/dev/accipiter/static/pointclouds/", shell=True )

      pcloud1 = pcloud(pagename=pagename)
      db.session.add(pcloud1)
      db.session.commit()

      return pagename

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadconvert():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      pagename = cloud_generate(secure_filename(f.filename))

      converted_url = "http://localhost:5000/" + pagename + ".html"
  # return 'your file ' + pagename + ' has been converted. View your ' + '<a href="http://localhost:5000/' + pagename + '.html">link</a>'
      return render_template("upload_complete.html", converted_url = converted_url)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
