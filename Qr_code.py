from flask import Flask,render_template,request,session
from DBConnection import Db
app = Flask(__name__)
app.secret_key = 'hi'




@app.route('/')
def admin_add_login():
    return render_template("login.html")

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form["textfield"]
    password = request.form["textfield2"]
    db=Db()
    qry="select * from login WHERE username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry)
    if res!=None:
        session['login_id']= res['lid']

        type=res['type']
        if type=='admin':
            return render_template("admin/admin_home.html")

        else:
            return '''<script>alert('Invalid User');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/'</script>'''


if __name__ == '__main__':
    app.run(debug=True)