from flask import Flask, render_template, url_for

app = Flask(__name__)

posts =[
    {
        'author': 'Corey Schafer',
        'title': 'blog post 1',
        'content': "dumb",
        'date_posted': 'May 1st, 2019'
    },
    {
        'author': 'John Doe',
        'title': 'blog post 2',
        'content': "dumber",
        'date_posted': 'April 20th, 2020'
    }
]


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")


if __name__ == "__main__":
    app.run(debug=True)