from flask import *
from database import *
import uuid



public=Blueprint('public',__name__)


@public.route('/')
def home():
    return render_template("home.html")


@public.route('/login', methods=['POST','GET'])
def login():
    if 'submit' in request.form:
        username = request.form['username']
        password = request.form['password']

        qry="select * from login where username='%s' and password='%s'"%(username, password)
        res=select(qry)

        if res:
            session['log']=res[0]['login_id']

            if res[0]['usertype'] == 'admin':
                return redirect(url_for('admin.admin_home'))
            
            if res[0]['usertype'] == 'police_station':
                qry1="select * from police_station where login_id='%s' "%(session['log'])
                res1=select(qry1)
                if res1:
                    session['police']=res1[0]['police_station_id']
                    return redirect(url_for('police.police_home'))          
        else:
            return '<script>alert("Please enter valid username & password");window.location="/login"</script>'
    return render_template("login.html")