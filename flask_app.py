#!app/bin/python
# Realmeister, at work...

from flask import *
import os, time, datetime
from functools import wraps
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, TextField
from wtforms.validators import DataRequired
import qrcode
from PIL import Image
import urllib2
import StringIO
import flask_app

SECRET_KEY = '4f7cae8cd1736360b612454ba772a1a9ca113259ff03385f26c6b59ca03052f5'

RECAPTCHA_PUBLIC_KEY = '6LdZ8PwSAAAAAER1_ZyOneJftFrSyDnS21RMzpmy'
RECAPTCHA_PRIVATE_KEY = '6LdZ8PwSAAAAAJhsiEWtsW4qcwSjQmOIfo5FnJg'

os.environ['TZ']='America/Detroit'
time.tzset()
def itisnow():
    return str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%m-%d-%y @ %H:%M:%S EDT'))

now = itisnow()
wigs = ['Aeteon','Melissa','Jeri','Sandy','RealMaster','Lisa']
passpalabras = ['rtmouse01','realticketmouse','wolfcreekamp','00001111','psalms3']

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

class MyForm(Form):
    username = TextField('Username')
    recaptcha = RecaptchaField()

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/realticket')
def owelcome():
    return render_template('welcome.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to Log In first.')
            return redirect(url_for('log'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('log'))

@app.route('/hello')
@login_required
def ohello():
    import flask_app
    reload(flask_app)
    flash('The current Timestamp is: %s'% now)
    return render_template('hello.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    success = None
    if request.method == 'POST':
        if request.form['username'] not in wigs or request.form['password'] not in passpalabras:
            error = "Incorrect credentials. Please, try again."
        else:
            session['logged_in'] = True
            success = str(request.form['username'])
            flash('You are now signed in as %s'% success)
            return redirect(url_for('ohello'))
    return render_template('log.html', error=error)

@app.route('/qrc')
@login_required
def qrc():
    return render_template('qr.html')


@app.route('/qr')
@login_required
def qr():
    data = StringIO.StringIO()
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=1,
        )
    qr.add_data(request.args.get("text"))
    qr.make(fit=True)

    img = qr.make_image()
    img.save(data, 'png')
    return send_file(StringIO.StringIO(data.getvalue()), mimetype='image/png')

@app.route('/purchaseprocess')
@login_required
def purpro():
    return render_template('nov3.html')

@app.route('/ticketpurchase')
@login_required
def tikpur():
    return render_template('realticketdaemon.html')

@app.route('/ticket')
@login_required
def Rticket():
    return render_template('ticket.html')

@app.route('/RealTicket', methods=['GET','POST'])
@login_required
def realticket():
    nom = None
    hom = None
    zom = None
    fom = None
    eom = None
    com = None
    vom = None
    tom = None
    qom = None
    pom = None
    som = None
    if request.method == 'POST':
        nom = request.form['cname']
        hom = request.form['caddress']
        zom = request.form['zcode']
        fom = request.form['cphone']
        eom = request.form['cemail']
        com = request.form['cccnumber']
        vom = request.form['ccvc']
        tom = request.form['ticket']
        qom = request.form['tquantity']
        pom = request.form['cpin']
        som = request.form['dsignature']
        flash('You entered: Name:%s Address:%s ZipCode:%s Phone:%s Email:%s Card Number:%s Cvc:%s Ticket:%s Quantity:%s Pin:%s'% (nom, hom, zom, fom, eom, com, vom, tom, qom, pom))
        return redirect(url_for('Rticket'))

if __name__ == '__main__':
    app.run()
