# from flask import Flask, request, render_template

# # Flask constructor
# app = Flask(__name__)

# @app.route('/', methods=["GET", "POST"])
# def gfg():
#     ret = []
#     if request.method == "POST":
#         # getting input with name = year in HTML form
#         year = request.form.get('year')
#         ret.append(year)
#         # getting input with name = term in HTML form
#         term = request.form.get('term')
#         ret.append(term)
#         # return "hi there friends"
#     # return render_template("form.html")
#     return "<p>Hello, World!</p>"

# if __name__ == '__main__':
#     app.run()


from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
