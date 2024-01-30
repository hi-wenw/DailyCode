from flask import Flask, render_template_string, request, session, url_for, redirect

app = Flask(__name__)

app.secret_key = r'F12Zr47j\3yX R~X@H!jLwf/T'


@app.route('/')
def hello():
    return 'hello gaozi'


@app.route('/login')
def login():
    page = '''
    <form action="{{ url_for('do_login') }}" method="post">
        <p>name: <input type="text" name="user_name" /></p>
        <input type="submit" value="Submit" />
    </form>
    '''

    return render_template_string(page)


@app.route('/do_login', methods=['POST'])
def do_login():
    name = request.form.get('user_name')
    session['name'] = name
    return 'success'


@app.route('/show')
def show():
    return session['name']


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
