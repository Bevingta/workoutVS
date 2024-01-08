from flask import Flask, render_template, request, url_for, redirect
from views import views

app = Flask(__name__)

#going to access all the views in views with "/"
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)