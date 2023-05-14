from flask import Flask,render_template,url_for,request,flash, session , redirect , send_from_directory
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] ='uploads'
app.secret_key ='avekop'


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            if filename.endswith('.csv') or filename.endswith('xlsx'):
                file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                flash("File Uploaded Succesfullly") 
            else:
                flash("only csv or xlsx file supported")
                return redirect('/')
        if 'logged_in' not in session:
            session['logged_in'] = False
    return render_template('index.html' )

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Wrong username or password')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("admin.html",files = files)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/open/<filename>')
def open_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(path)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(path)
    else:
        return "Invalid Path or file"
    table_data = df.to_dict(orient='records')
    return render_template('table.html',table_data = table_data)

@app.route('/downlaod/<filename>')
def downlaod(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename,as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)