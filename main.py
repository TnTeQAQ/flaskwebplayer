from flask import Flask, request, render_template, redirect, url_for, session
from API import tokenAPI
import config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        pwd = request.values.get('pwd')
        if pwd == config.SECRET_KEY:
            token = tokenAPI.generate_token("guest", "123")
            session["token"] = token
            return redirect(url_for('video', url_path='#'))
        else:
            return render_template('login.html', msg="密码错误")

    return render_template('login.html')

@app.route('/err')
def err():
    return render_template('err.html')

@app.route('/video/<path:url_path>')
def video(url_path):
    token = session.get('token')
    if not tokenAPI.validate_token(token):
        return redirect(url_for("err"))
    global l
    l = os.listdir(config.filepath)
    for f in l:
        if '.' not in f:
            lt = os.listdir(config.filepath+'/'+f)
            l.remove(f)
            l += list(map(lambda x: f+'/'+x, lt))
    l.sort(key=lambda fn: os.path.getmtime(config.filepath+'/'+fn))
    return render_template('index.html', list=l, name=url_path)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
