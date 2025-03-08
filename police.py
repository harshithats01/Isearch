from flask import *
from database import *



police=Blueprint('police',__name__)


@police.route('/police_home')
def police_home():
    return render_template("police_home.html")



@police.route('/police_view_registered_case', methods=['POST','GET'])
def police_view_registered_case():
    data={}
    x="select * from cases inner join users using(user_id) where police_station_id='%s'"%(session['police'])
    y=select(x)
    if y:
        data['view']=y 

    if 'action' in request.args:
        action=request.args['action']
        case_id=request.args['id']
    
    else:
        action=None    

    if action=='update':
        qry="update cases set status='Closed' where case_id='%s'"%(case_id)
        update(qry)
        return '<script>alert("Updated case successfully");window.location="/police_view_registered_case"</script>'

            

    return render_template("police_view_registered_case.html",data=data)



@police.route('/police_view_users', methods=['POST','GET'])
def police_view_users():
    data={}
    x="select * from users "
    y=select(x)
    if y:
        data['view']=y 

    return render_template("police_view_users.html",data=data)