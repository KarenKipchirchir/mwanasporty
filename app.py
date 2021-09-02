# Create the flask object
from flask import Flask, render_template

app = Flask(__name__)  # __name__ means main


# print(__name__)  You can use this to check if your name == main
# this is the body of your project


# This slash represents your main page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/activewear')
def activewear():
    return render_template('activewear.html')


@app.route('/shoes')
def shoes():
    return render_template('shoes.html')


@app.route('/accessories')
def accessories():
    return render_template('accessories.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')

@app.route('/account')
def account():
    return render_template('signin.html')




# check
if __name__ == '__main__':
    app.run(debug=True)
