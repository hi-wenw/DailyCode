from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index2.html')


@app.route('/trun', methods=['POST'])
def trun():
    try:
        strs = request.form.get('sheet_token')
        for i in strs.split():
            if '.' in i:
                old_name = i
                new_name = 'yishou_data.' + i.split('.')[1] + '_7day'

        data = strs.replace(old_name, new_name)
    except:
        data = ''
    return render_template('trun.html', data=data)


@app.route('/back')
def back():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
