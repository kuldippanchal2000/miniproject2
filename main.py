from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/blogzdaily'
db = SQLAlchemy(app)


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a error it stuck"


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was a error"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html',friends=friends)

@app.route("/")
def home():
    return render_template('1stpage.html')

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a error it stuck"
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

@app.route("/contact_us", methods = ['GET', 'POST'])
def contact_us():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        message = request.form.get('message')
        entry = Contact_us(fname=name, phone_num = mobile, message = message, email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact_us.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/sign_up")
def sign_up():
    return render_template('signup.html')




class Contact_us(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone_num = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(), nullable=False)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())

    def __repr__(self):
        return '<Name %r' % self.id

app.run(debug=True)
