from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url = generate_short_url()

    link = Link(id=short_url, original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    link = Link.query.get(short_url)
    if link:
        return redirect(link.original_url)
    else:
        return "Shortened URL not found."

def generate_short_url():
    return shortuuid.uuid()[:8]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
