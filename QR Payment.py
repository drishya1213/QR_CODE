from flask import Flask, redirect, render_template, request, session,jsonify
import datetime
import demjson
from DBConnection import Db

from qr_split import QR_split

import datetime


syspath=r"D:\QrPayment\static\\"

app = Flask(__name__)
app.secret_key="abc"

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        u=request.form['Username']
        p=request.form['Password']
        db=Db()
        ss=db.selectOne("select * from login where user_name='"+u+"' and password='"+p+"'")
        if ss is not None:
            if ss['user_type']=='admin':
                session['lid']=ss['login_id']
                session['lg']='lin'
                return redirect('/admin')
            elif ss['user_type']=='store':
                session['lg'] = 'lin'
                session['lid'] = ss['login_id']
                s = db.selectOne("select * from store where store_id='" + str(session['lid']) + "'")
                return redirect('/store')
            else:
                return '<script>alert("user not exist");window.location="/"</script>'
        else:
            return '<script>alert("user not exist");window.location="/"</script>'



    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    session['lg']=""
    return redirect('/')




@app.route('/admin')
def admin():
    if session['lg']=="lin":
        return render_template("ADMIN/adminhome.html")
    else:
        return redirect('/')

@app.route('/view_store_admin')
def view_store_admin():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from login,store where store.store_id=login.login_id and login.user_type='pending'")
        return render_template("ADMIN/approve_reject_store.html",store=s)
    else:
        return redirect('/')


@app.route('/view_user')
def view_user():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select user.*,login.*,user.user_name as uname from user,login where user.user_id=login.login_id and login.user_type='user'")
        return render_template("ADMIN/Customer.html",store=s)
    else:
        return redirect('/')

@app.route('/approve/<k>')
def approve(k):
    db=Db()
    db.update("update login set user_type='store' where login_id='"+str(k)+"' ")
    return '<script>alert("store approved");window.location="/view_store_admin"</script>'

@app.route('/reject/<l>')
def reject(l):
    db = Db()
    db.delete("delete from login WHERE login_id='"+str(l)+"'")
    db.delete("delete from store WHERE store_id='"+str(l)+"'")
    return '<script>alert("store rejected");window.location="/admin"</script>'


@app.route('/view_store_admin1')
def view_store_admin1():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from login,store where store.store_id=login.login_id and login.user_type='store'")
        return render_template("ADMIN/approved_store.html",store=s)
    else:
        return redirect('/')


@app.route('/category', methods=['GET', 'POST'])
def category():
    if session['lg'] == "lin":
        if request.method == "POST":
            category = request.form['textfield']
            db = Db()
            db.insert("insert into category values('','"+category+"')")
            return '<script>alert("Category Added");window.location="/category"</script>'
        else:
            db = Db()
            res = db.select("select * from category")
            return render_template("ADMIN/add_category.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_category/<c_id>')
def delete_category(c_id):
    if session['lg'] == "lin":
        db=Db()
        db.delete("delete from category where category_id = '"+c_id+"'")
        return '<script>alert("Deleted Sucessfully");window.location="/category"</script>'
    else:
        return redirect('/')


@app.route('/view_complaint')
def view_complaint():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from user,complaint where complaint.sender_id=user.user_id order by date desc")
        return render_template("ADMIN/view_complaint.html",data=s)
    else:
        return redirect('/')

@app.route("/send_reply/<id>", methods=['get', 'post'])
def send_reply(id):
    if request.method=="POST":
        rep=request.form['textfield']
        db=Db()
        db.update("update complaint set reply='"+rep+"', reply_date=curdate() where complaint_id='"+id+"'")
        return "<script>alert('Reply sent');window.location='/view_complaint';</script>"
    else:
        return render_template("ADMIN/send_reply.html")
@app.route('/view_feedback')
def view_feedback():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from user,feedback,store where feedback.user_id=user.user_id and feedback.store_id=store.store_id")
        return render_template("ADMIN/view_feedback.html",rate=s)
    else:
        return redirect('/')


# @app.route('/change_pasword',methods=['GET','POST'])
# def change_pasword():
#     if session['lg'] == "lin":
#         if request.method == "POST":
#             o = request.form['textfield']
#             n = request.form['textfield2']
#             c = request.form['textfield4']
#             db=Db()
#             s=db.selectOne("select * from login where login_id='"+str(session['lid'])+"'")
#             pas=s['password']
#             if pas==o:
#                 if n==c:
#
#                     db.update("update login set password='"+c+"' where login_id='" + str(session['lid']) + "' ")
#                     return '<script>alert("password changed");window.location="/admin"</script>'
#                 else:
#                     return '<script>alert(" Re-enter password");window.location="/change_pasword"</script>'
#             else:
#                 return '<script>alert("password mismatch");window.location="/admin"</script>'
#
#         else:
#
#             return render_template("ADMIN/change password.html")
#     else:
#         return redirect('/')
#

# ---------------------------STORE
@app.route('/store')
def store():
    if session['lg'] == "lin":
        return render_template("STORE/storehomes.html")
    else:
        return redirect('/')




@app.route('/store_register',methods=['POST','GET'])
def store_register():
    if request.method=="POST":
        sname=request.form['name']

        splace=request.form['place']
        spost=request.form['post']
        spin=request.form['pin']

        # img=request.files['file1']
        # date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        # img.save(syspath+"store\\" + date + '.jpg')
        # p1 = "/static/store/" + date + '.jpg'
        dis=request.form['select']

        lic=request.form['lic']

        phone=request.form['phone']
        email=request.form['email']

        pas1 = request.form['pas1']
        pas2 = request.form['pas2']
        db=Db()
        if pas1==pas2:
            s=db.insert("insert into login VALUES ('','"+email+"','"+pas2+"','pending')")

            db.insert("insert into store (store_id,store_name,store_location,store_phone,store_email,place,post,pin,licenseno) VALUES ('"+str(s)+"','"+sname+"','"+dis+"','"+phone+"','"+email+"','"+splace+"','"+spost+"','"+spin+"','"+lic+"')")
            return '<script>alert("Registered");window.location="/"</script>'
        else:
            return '<script>alert("password mismatch");window.location="/store_reg"</script>'


    return render_template("store_reg.html")












@app.route('/view_profile')
def view_profile():
    if session['lg'] == "lin":
        db=Db()
        s=db.selectOne("select * from store where store_id='"+str(session['lid'])+"'")
        return render_template("STORE/profile_view.html",i=s)
    return redirect('/')





@app.route('/store_edit',methods=['POST','GET'])
def store_edit():
    if session['lg'] == "lin":
        if request.method=="POST":
            ss=request.form['store']
            # img=request.files['file1']
            # date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            # img.save(syspath+"\store\\" + date + '.jpg')
            # p1 = "/static/store/" + date + '.jpg'
            d=request.form['select']

            p=request.form['place']
            po=request.form['post']
            pin=request.form['pin']
            phone=request.form['phone']
            lic=request.form['lic']
            date1 = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

            # lic.save(syspath+"\license\\" + date1 + '.jpg')
            # p2 = "/static/license/" + date1 + '.jpg'
            db=Db()
            db.update("update store set store_name='" + ss + "',store_location='" + d + "',place='" + p + "',post='" + po + "',pin='" + pin + "',store_phone='" + phone + "',licenseno='"+lic+"' where store_id='" + str(  session['lid']) + "'")
            return '<script>alert("updated");window.location="/view_profile"</script>'
            # if request.files!=None:
            #     if img.filename != "" and lic.filename != "":
            #         session['pic']=p1
            #         db.update("update store set store_name='"+ss+"',image='"+p1+"',license='"+p2+"',district='"+d+"',place='"+p+"',post='"+po+"',pin='"+pin+"',phone='"+phone+"' where store_id='"+str(session['lid'])+"'")
            #         return '<script>alert("updated");window.location="/view_profile"</script>'
            #     if img.filename != "" or lic.filename != "":
            #         if img.filename != "":
            #             session['pic']=p1
            #             db.update(
            #                 "update store set store_name='" + ss + "',image='" + p1 + "',district='" + d + "',place='" + p + "',post='" + po + "',pin='" + pin + "',phone='" + phone + "' where store_id='"+str(session['lid'])+"'")
            #             return '<script>alert("updated");window.location="/view_profile"</script>'
            #         else:
            #             db.update("update store set store_name='" + ss + "',license='" + p2 + "',district='" + d + "',place='" + p + "',post='" + po + "',pin='" + pin + "',phone='" + phone + "' where store_id='"+str(session['lid'])+"'")
            #             return '<script>alert("updated");window.location="/view_profile"</script>'
            #     else:
            #         db.update("update store set store_name='" + ss + "',district='" + d + "',place='" + p + "',post='" + po + "',pin='" + pin + "',phone='" + phone + "' where store_id='"+str(session['lid'])+"'")
            #         return '<script>alert("updated");window.location="/view_profile"</script>'
            #
            # else:
            #     db.update("update store set store_name='" + ss + "',district='" + d + "',place='" + p + "',post='" + po + "',pin='" + pin + "',phone='" + phone + "' where store_id='"+str(session['lid'])+"'")
            #     return '<script>alert("updated");window.location="/view_profile"</script>'

        else:
            db=Db()
            res=db.selectOne("select * from store where store_id='"+str(session['lid'])+"'")
            return render_template("STORE/edit_profile.html",i=res)
    else:
        return redirect('/')

@app.route('/view_rating_store')
def view_rating_store():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from user,rating where rating.sender_id=user.user_id and rating.store_id='"+str(session['lid'])+"'")
        return render_template("STORE/view rating.html",rate=s)
    else:
        return redirect('/')
@app.route('/change_pasword_store',methods=['GET','POST'])
def change_pasword_store():
    if session['lg'] == "lin":
        if request.method == "POST":
            o = request.form['textfield']
            n = request.form['textfield2']
            c = request.form['textfield4']
            db=Db()
            s=db.selectOne("select * from login where login_id='"+str(session['lid'])+"'")
            pas=s['password']
            if pas==o:
                if n==c:

                    db.update("update login set password='"+c+"' where login_id='" + str(session['lid']) + "' ")
                    return '<script>alert("password changed");window.location="/store"</script>'
                else:
                    return '<script>alert(" Re-enter password");window.location="/change_pasword_store"</script>'
            else:
                return '<script>alert("password mismatch");window.location="/store"</script>'

        else:

            return render_template("STORE/change password.html")
    else:
        return redirect('/')





@app.route('/bill_report')
def bill_report():
    if session['lg'] == "lin":
        db = Db()
        ss = db.select("select product.price*booking.count1 as tamount,product.*,booking.*,master.*,user.* from product,booking,master,user where master.master_id=booking.master_id and booking.product_id=product.product_id and master.user_id=user.user_id    and product.store_id='" + str(session['lid']) + "' and m_status!='added to cart'")

        v = db.selectOne("select sum(product.price*booking.count1) as tamount from product,booking,master,user where master.master_id=booking.master_id and booking.product_id=product.product_id and master.user_id=user.user_id    and product.store_id='"+str(session['lid'])+"' and b_status='paid'")
        return render_template("STORE/view_bill_report.html",bill=ss,bll=v)
    else:
        return redirect('/')








@app.route('/view_user_bookings')
def view_user_bookings():
    db = Db()
    res = db.select("select booking_master.*,user.* from booking_master,user where booking_master.user_id=user.user_id and booking_master.store_id='"+str(session['lid'])+"' and booking_master.status='booked'")
    # res = db.select("select booking_master.*,user.* from booking_master,user,product,booking where booking_master.user_id=user.user_id and booking.product_id=product.id and booking_master.masterid=booking.master_id and product.store_id ='"+str(session['lid'])+"' and booking_master.status='booked' group by booking.master_id")
    print(res)
    return render_template('STORE/view_user_bookings.html', data=res)


@app.route('/view_order_items/<m_id>',methods = ['get','post'])
def view_order_items(m_id):
        db = Db()
        # res = db.select("select  booking.count1*product.price as total_price1,booking.*,master.*,product.*  from master,booking,product where master.master_id=booking.master_id and booking.product_id=product.product_id and master.master_id = '"+m_id+"' and product.store_id ='"+str(session['lid'])+"'")
        res = db.select("select  booking.bquantity*product.price as total_price1,booking.*,booking_master.*,product.*  from booking_master,booking,product where booking_master.masterid=booking.master_id and booking.product_id=product.id and booking_master.masterid = '"+m_id+"' and product.store_id ='"+str(session['lid'])+"'")

        res1 = db.selectOne("select sum(booking.bquantity*product.price) as sum_total from booking_master,booking,product  where booking_master.masterid=booking.master_id and booking.product_id=product.id and booking_master.masterid = '"+m_id+"' and product.store_id ='"+str(session['lid'])+"'")
        total = str(res1['sum_total'])
        print(total)

        return render_template('STORE/vew_order_items.html', data=res,data1 = total, mid=m_id)



@app.route('/view_user_payments')
def view_user_payments():
    db = Db()
    res = db.select("select booking_master.*,user.* from booking_master,user where booking_master.user_id=user.user_id and booking_master.store_id='"+str(session['lid'])+"' and booking_master.status='paid'")
    # res = db.select("select booking_master.*,user.* from booking_master,user,product,booking where booking_master.user_id=user.user_id and booking.product_id=product.id and booking_master.masterid=booking.master_id and product.store_id ='"+str(session['lid'])+"' and booking_master.status='booked' group by booking.master_id")
    print(res)
    return render_template('STORE/view_payments.html', data=res)



@app.route("/generate_qr/<mid>")
def generate_qr(mid):
    qr_obj= QR_split()
    bb = qr_obj.qr2vc(mid)
    print("Path   ",bb)
    print("Encryption phase completed")
    return render_template("STORE/show_QR.html", path=bb)

@app.route("/show_qr2")
def show_qr2():
    path="/static/temp_files/decrypted.png"
    return render_template("STORE/show_QR2.html", path=path)



@app.route('/add_product',methods=['POST','GET'])
def add_product():
    if session['lg'] == "lin":
        if session['lg'] == "lin":
            if request.method=="POST":
                p=request.form['textfield']
                d=request.form['textarea']
                img=request.files['fileField']
                date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                img.save(syspath+"\product\\" + date + '.jpg')
                p1 = "/static/product/" + date + '.jpg'
                pr=request.form['price']
                q=request.form['textfiel']
                ctg=request.form['catg']
                db=Db()


                db.insert("insert into product(name,des,price,quantity,store_id,photo,category_id) VALUES ('"+p+"','"+d+"','"+pr+"','"+q+"','"+str(session['lid'])+"','"+p1+"','"+ctg+"')")
                return '<script>alert("product added");window.location="/add_product"</script>'

            db = Db()
            res = db.select("select * from category")
            return render_template("STORE/add_product.html",data = res)
        else:
            return redirect('/')
    else:
        return redirect('/')





@app.route('/view_product')
def view_product():
    if session['lg'] == "lin":
        db=Db()
        ss=db.select("select * from product,category where product.category_id=category.category_id and store_id='"+str(session['lid'])+"'")

        return render_template("STORE/view_product.html",product=ss)
    else:
        return redirect('/')

@app.route('/edit_product/<k>',methods=['POST','GET'])
def edit_product(k):
    if session['lg'] == "lin":
        if request.method=="POST":
            p=request.form['textfield']
            d=request.form['textarea']
            img=request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            img.save(syspath+"product\\" + date + '.jpg')
            p1 = "/static/product/" + date + '.jpg'
            pr=request.form['price']
            q=request.form['textfiel']
            db=Db()
            if request.files!=None:
                if img.filename!="":
                    db.update("update  product set name='" + p + "',des='" + d + "',quantity='" + q + "',price='" + pr + "',photo='" + p1 + "' where id='"+str(k)+"'")
                    return '<script>alert("product updated");window.location="/view_product"</script>'
                else:
                    db.update(
                        "update  product set name='" + p + "',des='" + d + "',quantity='" + q + "',price='" + pr + "' where id='" + str(
                            k) + "'")
                    return '<script>alert("product updated");window.location="/view_product"</script>'

            else:
                db.update("update  product set name='" + p + "',des='" + d + "',quantity='" + q + "',price='" + pr + "' where id='" + str(
                        k) + "'")
                return '<script>alert("product updated");window.location="/view_product"</script>'

        else:
            db = Db()
            pro=db.selectOne("select * from product where id='"+str(k)+"'")


            return render_template("STORE/edit_product.html",i=pro)
    else:
        return redirect('/')

@app.route('/delete/<d>')
def delete(d):
    db=Db()
    db.delete("delete from product where id='"+str(d)+"'")
    return '<script>alert("product deleted");window.location="/view_product"</script>'


@app.route('/delivery/<d>')
def delivery(d):
    db=Db()
    db.update("update booking set  b_status='deliverd' where ordr_id='"+str(d)+"'")
    return '<script>alert("Delivery status updated");window.location="/bill_report"</script>'



@app.route('/view_payment_history',methods = ['get','post'])
def view_payment_history(m_id):
        db = Db()

        # res1 = db.selectOne("select sum(booking.bquantity*product.price) as sum_total from booking_master,booking,product  where booking_master.masterid=booking.master_id and booking.product_id=product.id and product.store_id ='"+str(session['lid'])+"' and booking_master.status = 'paid'")
        res1 = db.selectOne("select sum(booking.bquantity*product.price) as sum_total,booking_master.*,user.* from booking_master,booking,product,user where booking_master.masterid=booking.master_id and booking.product_id=product.id and product.store_id ='"+str(session['lid'])+"' and booking_master.status = 'paid' and user.user_id=booking_master.user_id")
        total = str(res1['sum_total'])
        print(total)

        return render_template('STORE/vew_order_items.html', data=res1)




# --------------------------------------------------USER

@app.route('/user')
def user():
    if session['lg'] == "lin":
        return render_template("USER/user.html")
    else:
        return redirect('/')

@app.route('/view_profile_user')
def view_profile_user():
    if session['lg'] == "lin":
        db=Db()
        s=db.selectOne("select * from user where user_id='"+str(session['lid'])+"'")
        return render_template("USER/profile_view.html",i=s)
    else:
        return redirect('/')



@app.route('/user_reg',methods=['POST','GET'])
def user_reg():
    if request.method=="POST":
        ss=request.form['store']

        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        d=request.form['select']
        e=request.form['email']
        p=request.form['place']
        po=request.form['post']
        pin=request.form['pin']
        phone=request.form['phone']
        img=request.files['file3']

        img.save(syspath + "user_reg\\" + date + '.jpg')
        p2 = '/static/user/' + date + '.jpg'
        pas1 = request.form['pas1']
        pas2 = request.form['pas2']
        db=Db()
        ss1=db.selectOne("select * from login where username='"+e+"'")
        if ss1 is  None:
            if pas1==pas2:
                s=db.insert("insert into login VALUES ('','"+e+"','"+pas2+"','user')")

                db.insert("insert into user VALUES ('"+str(s)+"','"+ss+"','"+d+"','"+p+"','"+po+"','"+pin+"','"+e+"','"+phone+"','"+p2+"')")
                return '<script>alert("Registered");window.location="/"</script>'
            else:
                return '<script>alert("password mismatch");window.location="/user_reg"</script>'
        else:
            return '<script>alert("user already exist");window.location="/user_reg"</script>'

    return render_template("customer_reg.html")
















@app.route('/view_rating_user')
def view_rating_user():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from user,rating,store where rating.sender_id=user.user_id and rating.store_id=store.store_id")
        return render_template("USER/view rating.html",rate=s)
    else:
        return redirect('/')
@app.route('/view_product_user/<k>')
def view_product_user(k):
    if session['lg'] == "lin":
        db=Db()
        session['stid']=k
        ss=db.select("select * from product where product.store_id='"+str(k)+"'")

        return render_template("USER/view_product.html",product=ss)
    else:
        return redirect('/')

@app.route('/view_store_user')
def view_store_user():
    if session['lg'] == "lin":
        db=Db()
        s=db.select("select * from login,store where store.store_id=login.login_id and login.usertype='store'")
        return render_template("USER/view_store.html",store=s)
    else:
        return redirect('/')




@app.route('/add_to_cart/<p>', methods=['POST', 'GET'])
def add_cart(p):
    if session['lg'] == "lin":
            if request.method == 'POST':
                q = request.form['textfield4']
                r_date = request.form['textfield']
                db = Db()
                n = db.selectOne("select * from product where product_id='" + str(p) + "'")
                print(n)
                c = n['quantity']
                a = int(c) - int(q)
                k = db.selectOne("select * from master where user_id='" + str(session['lid']) + "' and m_status='added to cart'")
                print(k)
                print(a)
                if a >= 0:
                    if k is None:
                        ss = db.insert(
                            "insert into master VALUES ('','" + str(session['lid']) + "',0,'added to cart',curdate())")
                        s=db.insert("insert into booking VALUES ('','" + str(ss) + "','" + str( p) + "',0,'" + q + "','added to cart')")
                        db.update("update product set quantity=quantity-('" + q + "') where product_id='" + str(p) + "'")
                        db.insert("insert into returned VALUES ('','" + str(s) + "','"+r_date+"')")

                        return '<script>alert("added to cart");window.location="/view_product_user/'+str(session['stid'])+'"</script>'

                    else:
                        m = k['master_id']
                        ss = db.selectOne("select * from booking where master_id='" + str(m) + "' and product_id='" + str(p) + "'")

                        if ss is None:

                            s=db.insert("insert into booking VALUES ('','" + str(m) + "','" + str( p) + "',0,'" + q + "','added to cart')")
                            db.insert("insert into returned VALUES ('','" + str(s) + "','" + r_date + "')")
                            db.update("update product set quantity=quantity-('" + q + "') where product_id='" + str(p) + "'")
                            return '<script>alert("added to cart");window.location="/view_product_user/'+str(session['stid'])+'"</script>'
                        else:
                            ordr = ss['ordr_id']
                            c = ss['count1']

                            tot = int(c)+ int(q)


                            db.update("update product set quantity=quantity-('" + q + "') where product_id='" + str(p) + "'")
                            db.update("update booking set count1='"+str(tot)+"' where ordr_id='" + str(ordr) + "'")
                            db.update("update returned set returned_date='"+r_date+"' where booking_id='"+str(ordr)+"'")
                            return '<script>alert("added to cart");window.location="/view_product_user/'+str(session['stid'])+'"</script>'
                else:
                    return '<script>alert("check quantity");window.location="/view_product_user/'+str(session['stid'])+'"</script>'

            else:
                return render_template("USER/add_quanity.html")
    else:
        return redirect('/')


@app.route('/view_cart')
def view_cart():
    if session['lg'] == "lin":
        db = Db()
        ss = db.select("select datediff(returned_date,date) as days,product.*,booking.*,master.* from returned,product,booking,master where returned.booking_id=booking.ordr_id and master.master_id=booking.master_id and booking.product_id=product.product_id and master.user_id='"+str(session['lid'])+"'  and m_status='added to cart'")

        print(ss)
        return render_template("USER/view_cart.html",cart=ss)
    else:
        return redirect('/')

@app.route('/increment/<p>')
def increment(p):
    db=Db()
    ss = db.selectOne("select * from booking where ordr_id='" + str(p) + "'")
    q = ss['count1']
    s = ss['product_id']
    k=db.selectOne("select * from product where product_id='"+str(s)+"'")
    c=k['quantity']
    if int(c)>=1:
        db.update("update booking set count1=(count1+1) where ordr_id='"+str(p)+"'")
        db.update("update product set quantity=(quantity-1) where product_id='"+str(s)+"'")
        return '<script>alert("one item added");window.location="/view_cart"</script>'
    else:
        return '<script>alert("the required quantity is not available");window.location="/view_cart"</script>'


@app.route('/decrement/<p>')
def decrement(p):
    db=Db()
    ss=db.selectOne("select * from booking where ordr_id='"+str(p)+"'")
    q = ss['count1']
    s=ss['product_id']
    if q < 2:
        return '<script>alert("one item is left if u want to cancel this order please click remove option");window.location="/view_cart"</script>'
    else:

        db.update("update booking set count1=(count1-1) where ordr_id='"+str(p)+"'")
        db.update("update product set quantity=(quantity+1) where product_id='"+str(s)+"'")
        return '<script>alert("one item removed");window.location="/view_cart"</script>'

@app.route('/remove/<p>')
def remove(p):
    db=Db()
    db.delete("delete from booking where ordr_id='"+str(p)+"'")
    return '<script>alert("item removed from your cart");window.location="/view_cart"</script>'





@app.route('/buy',methods=['POST','GET'])
def buy():
    if session['lg'] == "lin":
        if request.method=='POST':
            k=session['k']
            j=session['j']
            b=request.form['textfield']
            ifsc=request.form['textfield3']
            ac=request.form['acnt']
            db = Db()
            ss = db.selectOne("select * from bank where bank_name='" + b + "' and ifsc='" + ifsc + "' and account_no='" + ac + "' and user_id='" + str(session['lid']) + "'")
            print(ss)


            if ss is None:
                return '<script>alert("Account doesnt exist");window.location="/view_cart"</script>'

            else:
                a = int(ss['balance'])
                k1 = float(k)
                print(k1)
                print(a)
                b = a - k1
                print(b)

                print(j)

                if int(a)<int(k1):
                    return '<script>alert("Account balance not sufficient");window.location="/view_cart"</script>'
                else:
                    db.update("update bank set balance=balance-'"+str(k)+"' where user_id='"+str(session['lid'])+"'")

                    s=db.selectOne("select * from booking where ordr_id='"+str(j)+"' ")
                    print(s)
                    v=s['product_id']
                    h=s['master_id']
                    s=db.selectOne("select store_id from product where product_id='"+str(v)+"' ")
                    db.update("update bank set balance=balance+'" + str(k) + "' where user_id='" + str(s['store_id']) + "'")
                    db.update("update master set amount='"+str(k)+"',m_status='paid',date=curdate() where master_id='"+str(h)+"'")
                    db.update("update booking set total_price='"+str(k)+"',b_status='paid' where ordr_id='"+str(j)+"'")

                    return '<script>alert("order completed");window.location="/view_cart"</script>'
        else:
            return render_template("USER/payment.html")
    else:
        return redirect('/')



@app.route('/borrow/<p>/<j>')
def borrow(p,j):

    db = Db()

    db.update("update  booking set b_status='booked',total_price='"+str(p)+"' where ordr_id='"+str(j)+"'")
    ss=db.selectOne("select * from booking where ordr_id='"+str(j)+"'")
    m=ss['master_id']


    s = '{"Master_id" :' + str(m) + '}'
    # url = pyqrcode.create(s)

    import datetime
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    qee = qrcode.make(str(s))
    qee.save(syspath + "qrcode\\" + date + ".png")
    qee.save(syspath + "shared_qr\\" + date + ".png")
    path = '/static/shared_qr/'+date+'.png'

    db.update("update  master set m_status='borrowed',amount='"+str(p)+"',qr = '"+str(path)+"' where master_id='"+str(m)+"'")
    return '<script>alert("Borrowed");window.location="/view_cart"</script>'


@app.route('/return1/<p>')
def return1(p):
    db=Db()
    db.update("update  booking set b_status='returned' where ordr_id='"+str(p)+"'")
    ss=db.selectOne("select * from booking where ordr_id='"+str(p)+"'")
    p_id=ss['product_id']
    c=ss['count1']
    print(p_id,c)
    db.update("update  product set quantity=quantity+'"+str(c)+"' where product_id='"+str(p_id)+"'")

    return '<script>alert("Returned");window.location="/history"</script>'


@app.route('/history')
def history():
    if session['lg'] == "lin":
        db=Db()
        ss = db.select("select product.price*booking.count1 as tamount,product.*,booking.*,master.*,store.* from product,booking,master,store where master.master_id=booking.master_id and booking.product_id=product.product_id and master.user_id='"+str(session['lid'])+"'    and product.store_id=store.store_id and m_status!='added to cart'")

        return render_template("USER/booking_history.html",history=ss)
    else:
        return redirect('/')





@app.route('/user_edit',methods=['POST','GET'])
def user_edit():
    if session['lg'] == "lin":
        if request.method=="POST":
            ss=request.form['store']
            img=request.files['file1']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            img.save(syspath+"user_reg\\" + date + '.jpg')
            p1 = "/static/user/" + date + '.jpg'
            d=request.form['select']

            p=request.form['place']
            po=request.form['post']
            pin=request.form['pin']
            phone=request.form['phone']

            db=Db()
            if request.files!=None:

                    if img.filename != "":
                        session['pic']=p1
                        db.update(
                            "update user set username='" + ss + "',u_photo='" + p1 + "',u_district='" + d + "',u_place='" + p + "',u_post='" + po + "',u_pin='" + pin + "',u_phone='" + phone + "' where user_id='"+str(session['lid'])+"'")
                        return '<script>alert("updated");window.location="/view_profile_user"</script>'
                    else:
                        db.update("update user set username='" + ss + "',u_district='" + d + "',u_place='" + p + "',u_post='" + po + "',u_pin='" + pin + "',u_phone='" + phone + "' where user_id='"+str(session['lid'])+"'")
                        return '<script>alert("updated");window.location="/view_profile_user"</script>'
            else:
                    db.update("update user set username='" + ss + "',u_district='" + d + "',u_place='" + p + "',u_post='" + po + "',u_pin='" + pin + "',u_phone='" + phone + "' where user_id='"+str(session['lid'])+"'")
                    return '<script>alert("updated");window.location="/view_profile_user"</script>'


        else:
            db=Db()
            res=db.selectOne("select * from user where user_id='"+str(session['lid'])+"'")
            return render_template("USER/edit_profile.html",i=res)
    else:
        return redirect('/')


# @app.route('/online/<k>/<j>',methods=['GET','POST'])
# def online(k,j):
#     if request.method=="POST":
#         pay=request.form['RadioGroup1']
#         if pay=='online':
#             session['k']=k
#             session['j']=j
#             return redirect("/buy")
#         else:
#             return borrow(k,j)
#     else:
#         return render_templ

@app.route('/online_bank',methods=['post'])
def online_bank():
    bn=request.form['bn']
    accnt=request.form['acc']
    ifsc=request.form['iff']
    amnt=request.form['amn']
    msid=request.form['mid']
    db=Db()
    v=db.selectOne("select * from bank where bank_name='"+bn+"' and account_no='"+accnt+"' and pin='"+ifsc+"'")
    if v is not None:
        bb=v['balance']
        if float(amnt)>float(bb):
            return jsonify(status="insuff")
        else:
            bid=v['bank_id']
            t=float(bb)-float(amnt)
            db.update("update bank set balance='"+str(t)+"'  where bank_id='" + str(bid) + "'")
            result="update booking_master set status='paid' where masterid='"+ str(msid) +"'"
            q=db.update(result)
            return jsonify(status="ok")
    else:
        return jsonify(status="no")





# -------------------------------------------------------------------------------------------------------------------------------


@app.route('/andlogin',methods=['post'])
def andlogin():
    u=request.form['username']
    p=request.form['password']
    db=Db()
    querry = "select * from login where user_name='" + u + "' and password='" + p + "'"
    res = db.selectOne(querry)
    print(res)
    if res is not None:
        if res['user_type'] == "admin" or  res['user_type'] == "store":
            return jsonify(status="no")
        else:
            return jsonify(status="ok", lid=res['login_id'])
    else:
        return jsonify(status="no")

@app.route('/clogin',methods=['post'])
def clogin():
    db=Db()
    u=request.form['username']
    p=request.form['password']
    querry = db.selectOne("select * from login where user_name='" + u + "' and password='" + p + "'")
    print(querry)
    res={}
    if querry:
        res['status']="ok"
        res['type']=querry['user_type']
        res['lid']=querry['login_id']
        res['email']=querry['user_name']
        return demjson.encode(res)
    else:
        res['status']="none"
        return demjson.encode(res)


@app.route('/andprofile',methods=['post'])
def andprofile():
    id=request.form['id']
    db=Db()
    querry=db.selectOne("select * from user WHERE user_id='"+id+"'")
    if querry is not None:
        return jsonify(status="ok", data=querry)
    else:
        return jsonify(status="no")

@app.route('/andcomplaint', methods=['post'])
def andcomplaint():
        id = request.form['lid']
        complaint = request.form['complaint']
        db = Db()
        querry=db.insert("insert into complaint (complaint, date,sender_id,reply, reply_date) VALUES ('"+complaint+"',curdate(),'"+id+"','pending','pending')")
        if querry is not None:
            return jsonify(status="ok")
        else:
            return jsonify(status="no")


@app.route('/and_view_complaint', methods=['post'])
def and_view_complaint():
    id = request.form['id']
    db = Db()
    querry=db.select("select * from complaint where sender_id = '"+id+"'")
    print(id)
    if querry is not None:
        return jsonify(status="ok",data = querry)
    else:
        return jsonify(status="no")

@app.route('/and_view_stores', methods=['post'])
def and_view_stores():
    id = request.form['id']
    db = Db()
    querry=db.select("select * from store, login where login.login_id=store.store_id and login.user_type='store'")
    if querry is not None:
        return jsonify(status="ok",data = querry)
    else:
        return jsonify(status="no")



@app.route('/and_view_product', methods=['post'])
def and_view_product():
    sid = request.form['store_id']
    print(sid)
    db = Db()
    querry=db.select("select * from product where store_id='"+sid+"'")
    print(querry)
    if querry is not None:
        return jsonify(status="ok",data = querry)
    else:
        return jsonify(status="no")


@app.route('/and_registration', methods=['post'])
def and_registration():
    db = Db()
    name = request.form['name']
    place = request.form['place']
    print(place)
    post = request.form['post']
    pin = request.form['pin']
    district = request.form['district']
    phone = request.form['phone']
    email = request.form['email']
    # qry1 = "select * from login where user_name='" + email + "'"
    # res = db.selectOne(qry1)
    photo = request.files['pic']
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    photo.save(syspath+"user_reg\\" + date + '.jpg')
    path = "/static/user_reg/" + date + '.jpg'
    password = request.form['password']
    cpass = request.form['cpass']
    res1 = {}
    if password == cpass:
        qry = "insert into login VALUES ('','" + email + "','" + str(password) + "','user')"
        lid = db.insert(qry)
        qr = "insert into  `user`(user_id,user_name,place,post,pin,district,phone_number,email,photo) VALUES ('" + str(lid) + "','" + name + "','" + place + "','" + post + "','"+pin+"','" + district + "','" + phone + "','" + email + "','" + str(path) + "')"
        res = db.insert(qr)
        res1['status'] = 'ok'
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)


@app.route('/quantity_order',methods=['post'])
def quantity_order():
    pid=request.form['product_id']
    quantity=request.form['q']
    id=request.form['lid']
    db=Db()
    res=db.selectOne("select * from cart where user_id='"+id+"' and prod_id='"+pid+"'")
    if res is None:
        db.insert("insert into cart(user_id, prod_id, qty, date) values('"+id+"', '"+pid+"', '"+quantity+"', curdate())")
        return jsonify(status="ok")
    else:
        db.update("update cart set qty=qty+'"+quantity+"', date=curdate() where cart_id='"+str(res['cart_id'])+"'")
    return jsonify(status="ok")

@app.route('/and_view_cart',methods=['post'])
def and_view_cart():
    id=request.form['id']
    db=Db()
    tot=0
    res=db.select("select product.name, product.price, product.photo, cart.qty, product.price* cart.qty as amount, cart.date from cart, product where cart.prod_id=product.id and cart.user_id='"+id+"'")
    for i in res:
        tot=tot+int(i['amount'])

    return jsonify(status="ok", data=res, sum=tot)

    # else:
    #     res['status']="none"
    #     return demjson.encode(res)

@app.route('/onlinep',methods=['post'])
def onlinep():
    id=request.form['id']
    mid=request.form['mid']
    a=request.form['amount']
    print(a)
    db=Db()
    result="update booking_master set status='paid', total_amount='"+ a +"' where masterid='"+ mid +"'"
    q=db.update(result)

    print(q)
    res={}
    if q:
        res['status']="ok"
        return demjson.encode(res)
    else:
        res['status']="none"
        return demjson.encode(res)



@app.route('/and_view_orders',methods=['post'])
def and_view_orders():
    id=request.form['id']
    db=Db()
    # qry=db.select("select booking.bquantity*product.price as total_price,booking.*,product.*,booking_master.* from booking,product,booking_master where booking.master_id=booking_master.masterid and booking.product_id=product.id and booking_master.user_id='"+id+"' and booking_master.status='booked'")
    qry=db.select("select * from booking_master where user_id='"+id+"' and status='booked'")
    res={}
    if qry:
        res['status']="ok"
        res['data']=qry
        return demjson.encode(res)
    else:
        res['status'] = "no"
        return demjson.encode(res)


@app.route('/and_delete_cart_prdct',methods=['post'])
def and_delete_cart_prdct():
    id=request.form['q']
    db=Db()
    db.delete("delete from booking where booking_id ='"+id+"'")
    return jsonify(status = "ok")




@app.route('/offlinep',methods=['post'])
def ofp():
    id=request.form['id']
    db=Db()
    res=db.select("select product.store_id from cart, product where cart.prod_id=product.id and cart.user_id='"+id+"' group by product.store_id")
    for i in res:
        store_id=i['store_id']
        store_tot=0
        res2=db.select("select product.*, cart.qty, cart.cart_id, cart.prod_id, product.price*cart.qty as amount from product, cart where cart.prod_id=product.id and cart.user_id='"+id+"' and product.store_id='"+str(store_id)+"'")
        for k in res2:
            store_tot=store_tot+int(k['amount'])
        oid=db.insert("insert into booking_master(user_id, date, status, total_amount, store_id) values('"+id+"', curdate(), 'booked', '"+str(store_tot)+"', '"+str(store_id)+"')")
        for j in res2:
            cart_id=j['cart_id']
            prod_id=j['prod_id']
            qty=j['qty']
            db=Db()
            db.insert("insert into booking(product_id, bquantity, master_id) values('"+str(prod_id)+"', '"+str(qty)+"', '"+str(oid)+"')")
            db.delete("delete from cart where cart_id='"+str(cart_id)+"'")
    return jsonify(status="ok")

    print("$$$  ",mid, a)
    db=Db()
    # result="update booking_master set status='booked', total_amount='"+ a +"' where masterid='"+ mid +"'"
    result="update booking_master set status='booked' where masterid='"+ mid +"'"
    q=db.update(result)

    print(q)
    res={}
    if q:
        res['status']="ok"
        return demjson.encode(res)
    else:
        res['status']="none"
        return demjson.encode(res)


@app.route('/track_status',methods=['post'])
def track_status():
    id=request.form['id']
    bid=request.form['bookingid']
    print(bid)
    db=Db()
    qry=db.select("select * from track,booking,booking_master where track.order_id=booking.booking_id and booking.master_id=booking_master.masterid and booking_master.user_id='"+id+"' and booking.booking_id='"+bid+"'")
    print(qry)
    res = {}
    if qry:
        res['status'] = "ok"
        res['data'] = qry
        return demjson.encode(res)





@app.route('/add_chat',methods=['post'])
def add_chat():
    lid = request.form['lid']
    toid = request.form['toid']
    message = request.form['message']
    print(lid,toid,message)
    db=Db()
    q2="insert into chat(from_id,to_id,messsage,date)values('"+lid+"','"+toid+"','"+message+"',curdate())"
    res = db.insert(q2)
    res1 = {}
    res1['status'] = "Inserted"
    return demjson.encode(res1)

@app.route('/view_chat',methods=['post'])
def view_chat():
    lid = request.form['lid']
    toid = request.form['toid']
    lastid = request.form['lastid']
    print(lid,toid,lastid)
    db=Db()
    q2="select chat.* from chat where chat_id>'"+lastid+"' and ((from_id='"+lid+"' and to_id='"+toid+"') or (from_id='"+toid+"' and to_id='"+lid+"'))"
    res = db.select(q2)
    print(res)
    res1 = {}
    res1['status'] = "ok"
    res1['data'] = res
    return demjson.encode(res1)
@app.route('/view_staff',methods=['post'])
def view_chatcouncillor():

    # q = db.select("select * from subect_alloc,staff,subject,suballoctocourse where  suballoctocourse.suballoccourseid=subect_alloc.csuballocid and suballoctocourse.ssubid=subject.sub_id and staff.Staff_id=subect_alloc.staff_name and suballoctocourse.scid='"+str(cid)+"' group by staff.Staff_id ")
    # print(q, cid)
    db=Db()
    q=db.select("select * from store")

    res1 = {}
    res1['status'] = "ok"
    res1['data'] = q
    return demjson.encode(res1)


@app.route('/location_update',methods=['post'])
def location_update():
    place=request.form['place']
    lati=request.form['lati']
    logi=request.form['logi']
    id=request.form['id']
    # bid=request.form['bid']
    # print(id)
    # print(place,lati,logi)
    db=Db()
    s = db.select("select * from user")

    # print(p)
    if s is not None:
        p = db.selectOne("select * from location,user where user.user_id=location.user_id and user.user_id='"+id+"'")

        if p is not None:
            # print("hi")
            d=db.update("update location set date=curdate(),latitude='"+lati+"' , longitude='"+logi+"',place='"+place+"' where user_id='"+id+"'")
            res = {}
            if d:
                res['status'] = "ok"
                return demjson.encode(res)
            else:
                res['status'] = ""
                return demjson.encode(res)
        else:
            # print("jjj")
            ss=db.insert("insert into location VALUES ('','"+id+"',curdate(),'"+lati+"','"+logi+"','"+place+"')")
            res={}
            if ss:
                    res['status']="ok"
                    return demjson.encode(res)
            else:
                    res['status']=""
                    return demjson.encode(res)
    else:
        res={}
        res['status']=""
        return demjson.encode(res)



@app.route('/payment',methods=['post'])
def payment():
    key=request.form['key']
    print("helloooooo   ", key)
    qr_obj = QR_split()
    path=qr_obj.vc2qr(key)
    return jsonify(status='ok')


    # db=Db()
    # result="update booking_master set status='payment_sucess', total_amount='"+ a +"' where masterid='"+ mid +"'"
    # q=db.update(result)
    #
    # print(q)
    # res={}
    # if q:
    #     res['status']="ok"
    #     return demjson.encode(res)
    # else:
    #     res['status']="none"
    #     return demjson.encode(res)










if __name__ == '__main__':
    app.run(host = "0.0.0.0",port="3000")
