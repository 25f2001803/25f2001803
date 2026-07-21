from flask import Flask

# __name__ to determine the application root path so it can locate templates, static files , and other resources correctly
app = Flask(__name__)

# routes map a url to python function
@app.route("/")

#run whenever someone visits
def home():
    return "<h1>Welcome to Trekking Management Application<h1/>"

#to ensure the server starts only when app.py is run directly 
if __name__ == "__main__":
    #starts flask development server
    app.run(debug=True)