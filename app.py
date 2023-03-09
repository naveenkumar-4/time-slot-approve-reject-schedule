import os
from twilio.rest import Client
from unittest import result
from flask import Flask,render_template,request
import mysql.connector as mysql


db = mysql.connect(
    host='localhost',
    user='root',
    password='Naveenkumar@60',
    database='db'
)

cursor=db.cursor()

app=Flask(__name__)
@app.route('/')
def indexPage():
    return render_template('index.html')


@app.route('/collectdata',methods=['POST','GET'])
def collectData():
    name=request.form['name']
    name = name.lower().capitalize()
    mobile=request.form['mobile']
    dt=request.form['d&t']
    if name and mobile and dt:
        result="Thank You for filling the Form"
        storeData(name,mobile,dt)
        return render_template('index.html',res=result)
    else:
        result="Please Fill the Details"
        return render_template('index.html',res=result)

@app.route('/getdata',methods=['POST','GET'])
def datafromDb():
    cursor.execute('SELECT * from time_scheduler')
    result=cursor.fetchall()
    data=[]
    for i in result:
        data.append(i)
    print(data)
    return render_template('admin.html',res=data)

@app.route('/collectmobile',methods=['POST','GET'])
def mobileData():
    mobile=request.form['num']
    status=request.form['sts']
    s = ""
    print(mobile,"-",status)
    if status == "approve":
        s='Approved'
        sql='UPDATE time_scheduler set status = %s where mobile = %s'
        val=(s,mobile)
        cursor.execute(sql,val)
        db.commit()
        """sql='SELECT * from time_scheduler where mobile = %s'
        val=(mobile)
        cursor.execute(sql,val)
        r=cursor.fetchall()
        db.commit()
        account_sid = os.environ['AC4936ff1927a5aa586f52631661c3ec6e']
        auth_token = os.environ['e8f2e88a1580a73c4d2bb3ede64e6aa1']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Hey Mr/Mrs {}!. Your Meeting has been scheduled on {}'.format(r[0][0],r[0][2]),
            from_='+15617821710',
            to='+917780338855'
        )"""
        return render_template('admin.html',res1=s)
    elif status == "reject":
        s='Rejected'
        sql='UPDATE time_scheduler set status = %s where mobile = %s'
        val=(s,mobile)
        cursor.execute(sql,val)
        db.commit()
        """sql='SELECT * from time_scheduler where mobile = %s'
        val=(mobile)
        cursor.execute(sql,val)
        r=cursor.fetchall()
        db.commit()
        account_sid = os.environ['AC4936ff1927a5aa586f52631661c3ec6e']
        auth_token = os.environ['e8f2e88a1580a73c4d2bb3ede64e6aa1']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Hey Mr/Mrs {}!. Your Meeting has been rejected'.format(r[0][0]),
            from_='+15617821710',
            to='+917780338855'
        )"""
        return render_template('admin.html',res1=s)
    elif status == "assign":
        time=request.form['time']
        s='Approved'
        sql='UPDATE time_scheduler set status = %s, date_time = %s where mobile = %s'
        val=(s,time,mobile)
        cursor.execute(sql,val)
        # db.commit()
        # sql='UPDATE time_scheduler set date_time = %s where mobile = %s'
        # val=(time,mobile)
        # cursor.execute(sql,val)
        db.commit()
        """sql='SELECT * from time_scheduler where mobile = %s'
        val=(mobile)
        cursor.execute(sql,val)
        r=cursor.fetchall()
        db.commit()
        account_sid = os.environ['AC4936ff1927a5aa586f52631661c3ec6e']
        auth_token = os.environ['e8f2e88a1580a73c4d2bb3ede64e6aa1']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Hey Mr/Mrs {}!. Your Meeting has been scheduled on {}'.format(r[0][0],r[0][2]),
            from_='+15617821710',
            to='+917780338855'
        )"""
        return render_template('admin.html',res1=s)

@app.route('/checkStatus',methods=['POST','GET'])
def checkStatus():
    mobile=request.form['num']
    print(type(mobile))
    l=[]
    l.append(mobile)
    sql='SELECT * from time_scheduler where mobile = %s'
    value=l
    cursor.execute(sql,value)
    print(sql)
    result=cursor.fetchall()
    print(result)
    if result:
        r1=result[0][0]
        r2=result[0][1]
        r3=result[0][2]
        r4=result[0][3]
        if(r4=="Approved"):
            x="Mr./Ms."+ r1 +" Your application has been Approved and Your meeting is scheduled on "+ r3
            return render_template('index.html',res1=x)
        elif(r4=="Rejected"):
            x="Mr./Ms."+ r1 +"Your application has been "+ r4
            return render_template('index.html',res1=x)
        else:
            r5="Application is Still on Process"
            return render_template('index.html',res5=r5)
    else:
        return render_template('index.html',res5="Enter valid details")

def storeData(name,mobile,date_time):
    sql='INSERT INTO time_scheduler(name,mobile,date_time) VALUES(%s,%s,%s)'
    values=(name,mobile,date_time)
    cursor.execute(sql,values)
    db.commit()


if __name__ == "__main__":
    app.run(debug='True')
    
