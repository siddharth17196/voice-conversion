from flask import Flask, Response, render_template, request
import os
from werkzeug.utils import secure_filename
# import getpreds
# import test

upload_folder = 'static'
allowed_extensions = ['jpeg' ,'jpg', 'png']

app = Flask(__name__)
app.config['upload_folder'] = upload_folder
app.config["ALLOWED_AUDIO_EXTENSIONS"] = ["MP3", "WAV"]

def allowed_filename(filename):
	if not "." in filename:
		return False
	ext = filename.rsplit(".", 1)[1]
	if ext.upper() in app.config["ALLOWED_AUDIO_EXTENSIONS"]:
		return True
	else:
		return False

@app.route('/')
def index_view():
    return render_template('about_proj.html')

@app.route('/about')
def about_view():
    return render_template('about.html')

@app.route('/predict', methods=['GET','POST'])
# def predict():
#     response = "For conversion"
#     return render_template('upload_audio.html')
def upload():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            img_loc = os.path.join(app.config['upload_folder'], filename)
            file = request.files['file']
            file.save(upload_folder+'/'+'snek.wav')
            print(img_loc)
            test.get_pred()
            # return render_template()
    return render_template('upload_audio.html')

@app.route("/play/conv")
def streamwav_conv():
    def generate():
        with open("static/conv/snek.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/wav")

@app.route("/play/src")
def streamwav_src():
    def generate():
        with open("static/snek.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/wav")

if __name__ == "__main__":
    app.run()
