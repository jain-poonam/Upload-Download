import os
from flask import Flask,flash,render_template,jsonify,request,redirect, send_from_directory,url_for
from werkzeug.utils import secure_filename
from fileinput import filename

Upload_Path ="/Users/pyjain/Documents/Assignment4"
EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = Upload_Path
app.config["MAX_CONTENT_LENGTH"] = 20*1024*1024

def check_extension(file):
    name,ext=os.path.splitext(file)
    if ext.lower() in EXTENSIONS:
        return True
    else:
        return False


@app.route("/")
def start_upload():
    return render_template("start.html")

@app.route("/",methods=["POST"])
def upload_file():
    if "file" not in request.files:       
        return render_template("start.html",error= "No file")
    input = request.files["file"]
    if input.filename == "":
        return render_template("start.html",error= "Empty file")
    if input and check_extension(input.filename):
        filename = secure_filename(input.filename)
        input.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        stat=os.stat(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        
        return render_template("function.html",result=input.filename,size=stat.st_size)
    else:
        return render_template("start.html",error= "Invalid Extension")
    
    
@app.route("/view",methods=["POST","GET"])
def view_files():
    list1=[]
    for filename in os.listdir(Upload_Path):
        path=os.path.join(Upload_Path,filename)
        if os.path.isfile(path):
            list1.append(filename)
    return render_template("list.html", result=list1)
    


@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)
         
@app.route("/delete/<filename>")
def delete_files(filename):
    os.remove(Upload_Path +"/" + filename)
    return redirect(url_for("view_files"))
                  
                        
if __name__ == "__main__":
    app.run()
