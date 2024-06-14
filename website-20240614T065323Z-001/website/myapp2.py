from flask import Flask,render_template,redirect
import pymysql as p

def getconnect():
    return p.connect(host="localhost", user="root", password="",database="batch2023")
def getdata():
    db=getconnect()
    cr=db.cursor()

    sql="select name,password from student"
    cr.execute(sql)
    data=cr.fetchall()

    db.commit()
    db.close()
    return data

def insertdata(t):
    db=getconnect()
    cr=db.cursor()

    sql="insert into student values(%s,%s,%s,%s,%s)"
    cr.execute(sql,t)
    data=cr.fetchall()
    db.commit()
    db.close()

def getalldata():
    db=getconnect()
    cr=db.cursor()
    sql ="select * from student"
    cr.execute(sql)
    data=cr.fetchall()
    db.commit()
    db.close()
    return data

def getbyids(ids):
    db=getconnect()
    cr=db.cursor()
    sql ="select * from student where id=%s"
    cr.execute(sql,ids)
    data=cr.fetchone()
    db.commit()
    db.close()
    return data

def updatedata(t):
    db=getconnect()
    cr=db.cursor()

    sql="update student set name=%s, email=%s, address=%s, password=%s where id=%s"
    cr.execute(sql,t)
    db.commit()
    db.close()

def deletedata(ids):
    db=getconnect()
    cr=db.cursor()
    sql="delete from student where id=%s"
    cr.execute(sql,ids)
    db.commit()
    db.close()




app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/Log in")
def log():
    return render_template("page1.html")

@app.route("/Shirts for all")
def shirts():
    return render_template("shirts.html")
@app.route("/festival collection")
def festival():
    return render_template("festivalseason.html")

@app.route("/registration")
def register():
    return render_template("page2.html")

@app.route("/validateuser", methods=["POST"])
def valid_user():
    usern=request.form["uname"]
    pasw=request.form["pin"]

    data=(usern, pasw)
    database=getdata()

    if(data in database):
        return render_template("home.html")
    else:
        return render_template("page2.html")

@app.route("/insertrec",methods=["POST"])
def signup():
    ids=request.form["id"]
    uname=request.form["uname"]
    email=request.form["email"]
    add=request.form["address"]
    passw=request.form["pin"]

    t=(ids,uname,passw,email,add)
    insertdata(t)
    return render_template("home.html")
@app.route("/users")
def user_list():
    ulist=getalldata()
    return render_template("users.html",u = ulist)

@app.route("/updateuser/<int:ids>")
def update_user(ids):
    a=getbyids(ids)
    return render_template("edituser.html",data=a)

@app.route("/updaterec", methods=["POST"])
def update_rec():
    ids=request.form["id"]
    uname=request.form["uname"]
    email=request.form["email"]
    add=request.form["address"]
    passw=request.form["pin"]

    t=(uname,email,add,passw,ids)
    updatedata(t)

    return redirect("/users")

@app.route("/deleteuser/<int:ids>")
def delete_rec(ids):
    deletedata(ids)
    return redirect("/users")



if(__name__=="__main__"):
    app.run(debug=True)
