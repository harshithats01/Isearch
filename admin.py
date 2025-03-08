from flask import *
from database import *



admin=Blueprint('admin',__name__)


@admin.route('/admin_home')
def admin_home():
    return render_template("admin_home.html")
    


@admin.route('/admin_manage_police_station', methods=['POST','GET'])
def admin_manage_police_station():
    data={}
    x="select * from police_station "
    y=select(x)
    if y:
        data['view']=y 


    if 'action' in request.args:
        action=request.args['action']
        login_id=request.args['id']
    
    else:
        action=None

    if action=='delete':
        a="delete from police_station where login_id='%s'"%(login_id)
        delete(a)

        qry="delete from login where login_id='%s'"%(login_id)
        delete(qry)
        return '<script>alert("Police station deleted successfully");window.location="/admin_manage_police_station"</script>'
    

    if action=='update':
        z="select * from police_station where login_id='%s'"%(login_id)
        res=select(z)
        data['up']=res


    if 'update' in request.form:
        pname = request.form['pname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        pin = request.form['pin']
        a="update police_station set police_station_name='%s',place='%s',phone='%s',email='%s',pin='%s' where login_id='%s'"%(pname,place,phone,email,pin,login_id)
        update(a)
        return '<script>alert(" Police Station details Updated successfully");window.location="/admin_manage_police_station"</script>'


    if 'submit' in request.form:
        pname = request.form['pname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        pin = request.form['pin']
        username = request.form['username']
        password = request.form['password']

        qry3="insert into login values(null,'%s','%s','police_station')"%(username,password)
        res3=insert(qry3)

        qry2="insert into police_station values(null,'%s','%s','%s','%s','%s','%s')"%(res3,pname,place,phone,email,pin)
        insert(qry2) 
        return ("<script>alert('Police station details Added Successfully');window.location='/admin_manage_police_station'</script>")

    return render_template("admin_manage_police_station.html",data=data)


@admin.route('/admin_view_users', methods=['POST','GET'])
def admin_view_users():
    data={}
    x="select * from users "
    y=select(x)
    if y:
        data['view']=y 

    return render_template("admin_view_users.html",data=data)




@admin.route('/admin_view_complaints', methods=['POST', 'GET'])
def admin_view_complaints():
    data={}
    a = "select * from complaints inner join users using(user_id)"
    b=select(a)
    if b:
        data['view']=b

    if 'reply' in request.form:
        complaint_id = request.form['complaint_id']
        reply = request.form['reply']
        qry = "update complaints set reply='%s' where complaint_id='%s'" % (reply, complaint_id)
        update(qry)
        return '<script>alert("Reply sent successfully"); window.location="/admin_view_complaints"</script>'     
    return render_template("admin_view_complaints.html",data=data)


@admin.route('/admin_view_feedback')
def admin_view_feedback():
    data={}
    x="select * from feedback inner join users using(user_id)"
    y=select(x)
    if y:
        data['view']=y 
    return render_template("admin_view_feedback.html", data=data)