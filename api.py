import os
import shutil
import uuid
from flask import * 
from database import*

api=Blueprint('api',__name__)


@api.route('/api_register')
def api_register():
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    email=request.args['email']
    phone=request.args['phone']
    gender=request.args['gender']
    place=request.args['place']
    address=request.args['address']
    username=request.args['username']
    password=request.args['password']



    qr1="select * from users where email='%s'"%(email)
    r1=select(qr1)
    if r1:
        data['status']="already"
    else:
        qry3="insert into login values(null,'%s','%s','user')"%(username,password)
        res3=insert(qry3)

        qry2="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(res3,fname,lname,email,phone,gender,place,address)
        res2=insert(qry2) 
        if res2:
            data['status']="success"
        else:
            data['status']="failed"
    return str(data)






@api.route('/apilogin')
def login():
    data={}
    username = request.args['uname']
    password = request.args['password']
    qry="select * from login where username='%s' and password='%s'"%(username, password)
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="login"
    return str(data)




@api.route('/api_view_stations')
def api_view_stations():
    data={}
    qry="select * from police_station"
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    return str(data)


@api.route('/send_feedback')
def send_feedback():
    data={}
    loginid=request.args['loginid']
    feedback=request.args['feedback']
    
    qry="insert into feedback values(null,(select user_id from users where login_id='%s'),'%s',curdate())"%(loginid,feedback)
    res=insert(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="feedback"
    return str(data)



@api.route('/apicom')
def apicom():
    data={}
    title=request.args['title']
    com=request.args['com']
    userid=request.args['loginid']
    
    qry="insert into complaints values(null,(select user_id from users where login_id='%s'),'%s','%s','pending',curdate())"%(userid,title,com)
    res=insert(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="com"
    return str(data)



@api.route('/apiviewcom')
def apiviewcom():
    data={}
    loginid=request.args['loginid']
    qry="select * from complaints where user_id=(select user_id from users where login_id='%s')"%(loginid)
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    return str(data)


# from face_model import *
# @api.route('/add_case',methods=['post'])
# def add_case():
  
#     title= request.form['title']
#     description = request.form['description'] 
#     police_id=request.form['police_id']
#     user_id=request.form['user_id']
 

#     img = request.files['image']
#     path = "static/images/"+str(uuid.uuid4())+img.filename
#     img.save(path) 

#     q = "insert into cases values(null,'%s',(select user_id from users where login_id='%s'),'%s','%s','%s',curdate(),'pending')"%(police_id,user_id,title,description,path) 
#     bid=insert(q)
    
#     pid = str(bid)
#     train_images_folder = os.path.join("static", "trainimages", pid)
    
#     if not os.path.isdir(train_images_folder):
#             os.makedirs(train_images_folder)

#         # Copy the image to the trainimages folder three times with different names
#     for i in range(1, 4):  # Loop three times
#         destination_image_path = os.path.join(train_images_folder, f"{os.name}_{i}.jpg")
#         shutil.copy(path, destination_image_path)
#         break

        
#     enf("static/trainimages/")

#     return jsonify(status="ok") 



from face_model import *
@api.route('/add_case',methods=['post'])
def add_case():
  
    fir_no= request.form['fir_no']
    place = request.form['place'] 
    act= request.form['act']
    occurance = request.form['occurance'] 
    description=request.form['description']
    police_id=request.form['police_id']
    user_id=request.form['user_id']
 

    img = request.files['image']
    path = "static/images/"+str(uuid.uuid4())+img.filename
    img.save(path) 

    q = "insert into cases values(null,'%s',(select user_id from users where login_id='%s'),'%s','%s','%s',curdate(),'pending','%s','%s','%s')"%(police_id,user_id,fir_no,place,path,act,occurance,description) 
    bid=insert(q)
    
    pid = str(bid)
    train_images_folder = os.path.join("static", "trainimages", pid)
    
    if not os.path.isdir(train_images_folder):
            os.makedirs(train_images_folder)

        # Copy the image to the trainimages folder three times with different names
    for i in range(1, 4):  # Loop three times
        destination_image_path = os.path.join(train_images_folder, f"{os.name}_{i}.jpg")
        shutil.copy(path, destination_image_path)
        break

        
    enf("static/trainimages/")

    return jsonify(status="ok")


@api.route('/view_mycase')
def view_mycase():
    data={}
    id=request.args['id']
    
    qry="select * from cases where user_id=(select user_id from users where login_id='%s')"%(id)
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    return str(data)


from core import *
@api.route('/check_person',methods=['get','post'])
def check_person():
    data={}
    image=request.files['image']
    lati=request.form['lati']
    longi=request.form['longi']
    image.save("static/images/" + "test.jpg")
    path="static/images/" + "test.jpg"
    qh=rec_face_image(path)
    if qh:
        print(qh,"---------------")
        q="select * from cases where case_id='%s'"%(qh[0])
        r=select(q)
        print(r,"---------------------")
        qr1="insert into alert values(null,'%s','%s','%s','%s',curdate(),curtime())"%(qh[0],path,lati,longi)
        r1=insert(qr1)
        if r1:
            data['status']="success"
            data['data']="person matching with case"+r[0]['description'] 
        else:
            data['status']="failed"
        return str(data)
        
        
        
        
        
@api.route('/view_allcase')
def view_allcase():
    data={}

    
    qry="select * from cases"
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    return str(data)


@api.route('/view_found')
def view_found():
    data={}
    id=request.args['id']
    qry="select * from alert where case_id='%s'"%(id)
    res=select(qry)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    return str(data)
    
    
    
    
@api.route('/view_alert')
def view_alert():
    data={}
    id=request.args['id']
    
    qry = "SELECT * FROM alert INNER JOIN cases USING(case_id) INNER JOIN users USING(user_id) WHERE users.login_id='%s' AND alert.date = CURDATE() AND TIME_FORMAT(time, '%%H:%%i') = TIME_FORMAT(CURTIME(), '%%H:%%i')" % (id)
    res=select(qry)
    print(res,"===="*100)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="alert"
    return str(data)
    
    
    
    



import smtplib
import random
import string
from flask import Flask, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@api.route('/api_forgot')
def forget():
    data = {}
    Email = request.args.get('email')  # Use get() to prevent KeyError

    if not Email:
        return jsonify({"status": "failed", "message": "Email parameter is required", "method": "forgot"})

    qry = "SELECT * FROM users WHERE Email='%s'" % (Email)
    res = select(qry)  # Assuming select() function is defined

    if res:
        # Generate a 6-digit verification code
        verification_code = ''.join(random.choices(string.digits, k=6))

        # Send verification code via email
        email_sent = send_mail(Email, verification_code)

        if email_sent:
            data['status'] = "success"
            data['data'] = res
            data['verification_code'] = verification_code  # Add generated code
        else:
            data['status'] = "failed"
            data['message'] = "Failed to send verification email"
    else:
        data['status'] = "failed"
        data['message'] = "Email not found"

    data['method'] = "forgot"

    return jsonify(data)

def send_mail(to_email, verification_code):
    try:
        sender_email = "hariharan0987pp@gmail.com"
        sender_password = "rjcbcumvkpqynpep"  # Use App Password for security

        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = 'Password Reset Verification Code'

        # Email Body with Verification Code
        body = f"Your password reset verification code is: {verification_code}\n\nUse this code to reset your password."
        msg.attach(MIMEText(body, 'plain'))

        gmail.send_message(msg)
        gmail.quit()
        print("Email sent successfully")
        return True  # Email sent successfully

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        return False  # Email sending failed



@api.route('/new_password')
def new_password():
    data={}
    login_id=request.args['id']
    Confirm=request.args['Confirm']


    qry="update login set password='%s' where login_id='%s'"%(Confirm,login_id)
    res=update(qry)
    if res:
        data['status']='success'

    else:
        data['status']="failed"
    data['method']="update_pass"

    return str(data)




@api.route('/update_password')
def update_password():
    data={}
    newPassword=request.args['newPassword']
    id=request.args['id']

    qry="update login set password='%s' where login_id='%s'"%(newPassword,id)
    res=update(qry)
    if res:
        data['status']="success"
    else:
        data['status']="failed"
    data['method']="update_pass"
    return str(data)