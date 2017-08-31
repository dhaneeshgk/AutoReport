from flask import Flask, render_template, request, make_response,redirect,url_for,send_file,flash,Markup
from api_requests import apis
from werkzeug import secure_filename
import os

app = Flask(__name__)

app.secret_key = 'random string'

@app.route('/')
def index():
    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if con["status"]:
            return redirect(url_for("home"))
    res = apis.set_up()
    return redirect("/login")

@app.route('/login',methods = ['GET'])
def login():
    return render_template("login.html")

@app.route('/login')
def re_login():
    return render_template("login.html",text="Invalid Credentials")

@app.route('/home',methods=['GET','POST'])
def home():
    email_ = None
    password_ = None
    if request.method == 'POST':
        email_ = request.form['email_name']
        password_ = request.form['password']
        con = apis.login(email_.lower(),password_)
        # print(con)
        if con["status"]:
            flash(con['remarks'])
            if con['token_type']=='u':
                resp = make_response(render_template('navpage.html'))
            elif con['token_type']=='a':
                resp = make_response(render_template('navpage_admin.html'))
            resp.set_cookie("auto_report_wp",con["access_token"])
            resp.set_cookie("token_type",con["token_type"])
            # flash(Markup('Successfully registered, please click <a href="/me" class="alert-link">here</a>'))
            return resp
        else:
            flash(con['remarks'])
            return redirect(url_for('re_login'))
    else:
        if 'auto_report_wp' in request.cookies:
            con = apis.validate_auth(request.cookies.get('auto_report_wp'))
            if con["status"]:
                if request.cookies['token_type']=='u':
                    return render_template('navpage.html')
                elif request.cookies['token_type']=='a':
                    return render_template('navpage_admin.html')
        else:
            flash("Your session is expired")
            return redirect(url_for('login'))

@app.route("/home")
def back_home():
    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if con["status"]:
            return render_template('navpage.html')
    return redirect(url_for('login'))

@app.route('/envs',methods=['GET','POST','PUT','DELETE'])
def envs():
    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if not con["status"]:
            flash("Your session is expired")
            return redirect(url_for('login'))
    else:
        flash("Your session is expired")
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template("envs.html",
        envs=apis.get_envs(request.cookies['auto_report_wp'])["environments"])
    elif request.method == 'POST':
        if "do" in request.form:
            if request.form['do']=="add":
                data = {i:request.form[i] for i in request.form if not i in ["do"]}
                # print(data)
                res = apis.add_environemt(request.cookies['auto_report_wp'],data=data)
                # print(res)
                if res['status']:
                    flash(res['remarks'])
                else:
                    flash(res['error'])
        elif "delete" in request.form.values():
            data = {'environment':list(request.form.keys())[0]}
            res = apis.delete_environment(request.cookies['auto_report_wp'],data=data)
            flash(res['remarks'])
        elif "down" in request.form:
            # print(request.form)
            res = apis.get_scheduled_tasks(request.cookies['auto_report_wp'],data={"environment":request.form["down"]})
            # print(res)
            if 'tasks' in res:
                if res['tasks']:
                    vms = [i['vm'] for i in res['tasks'] if i["status"]=="Y"]
                else:
                    vms = []

                if not vms:
                    res = apis.update_environment(request.cookies['auto_report_wp'],data={
                    "environment":request.form["down"],"status":"DOWN"})
                else:
                    for i in vms:
                        res_u = apis.updates(request.cookies['auto_report_wp'],data={"vm":i,"stop_vm":"Y",
                        "start_vm":"N"})

                    vms = True
                    while vms:
                        res = apis.get_scheduled_tasks(request.cookies['auto_report_wp'],
                            data={"environment":request.form["down"]})

                        if 'tasks' in res:
                            if res['tasks']:
                                vms = [i['vm'] for i in res['tasks'] if i["status"]=="R"]
                            else:
                                vms = []

                    res = apis.update_environment(request.cookies['auto_report_wp'],data={
                    "environment":request.form["down"],"status":"DOWN"})
                flash("Thank you for intimating '{0}' server status , all the scheduled auomation running on '{0}' environment have been stopped now".format(request.form["down"]))

        elif "up" in request.form:
            res = apis.get_scheduled_tasks(request.cookies['auto_report_wp'],data={"environment":request.form["up"]})
            # print(res)
            if 'tasks' in res:
                if res['tasks']:
                    vms = [i['vm'] for i in res['tasks'] if i["status"]=="S"]
                else:
                    vms = []

                if not vms:
                    res = apis.update_environment(request.cookies['auto_report_wp'],data={
                    "environment":request.form["up"],"status":"UP"})
                else:
                    for i in vms:
                        res_u = apis.updates(request.cookies['auto_report_wp'],data={"vm":i,"stop_vm":"N",
                        "start_vm":"Y"})

                    res = apis.update_environment(request.cookies['auto_report_wp'],data={
                    "environment":request.form["up"],"status":"UP"})
                flash("Thank you intimating '{0}' server  status, all the scheduled automation will be resumed now".format(request.form["up"]))

    return render_template("envs.html",
    envs=apis.get_envs(request.cookies['auto_report_wp'])["environments"])



@app.route("/schedules",methods=['GET','POST'])
def schedules():
    fill_i = {}
    # print(request.form)
    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if not con["status"]:
            return redirect(url_for('login'))


    if request.method == 'POST':
        if "do" in request.form:
            if request.form["do"] == "add":
                data = {i:request.form[i] for i in request.form if not i in ['do']}
                # print(data)
                res = apis.add_schedules_tasks(access_token=request.cookies['auto_report_wp'],data=data)
                if res["status"]:
                    flash(res["remarks"])
                flash(res["remarks"])

        elif "delete" in request.form:
                data = {"task":request.form["delete"]}
                res = apis.delete_schedules_tasks(access_token=request.cookies['auto_report_wp'],data=data)
                if res["status"]:
                    flash(res["remarks"])
                flash(res["remarks"])


        elif "edit" in request.form:
            print("in edit")
            data = {"task":request.form['edit']}
            schedule = apis.get_scheduled_tasks(access_token=request.cookies['auto_report_wp'],data=data)
            # print(schedule)
            fill_i = schedule['task']
            print(fill_i)

        elif "update" in request.form:
            gdata = {"task":request.form["update"]}
            # print(gdata)
            schedule = apis.get_scheduled_tasks(access_token=request.cookies['auto_report_wp']
            ,data=gdata)
            # print(schedule)
            data = {i:request.form[i] for i in request.form if not i in ['update']}
            data.update({"id":schedule["task"]["id"],"task":request.form["update"]})
            # print(data)
            res = apis.update_scheduled_tasks(access_token=request.cookies['auto_report_wp'],data=data)
            # print(res)
            if res["status"]:
                flash(res["remarks"])
            flash(res["remarks"])



    schedules = apis.get_scheduled_tasks(access_token=request.cookies['auto_report_wp'])
    envs = apis.get_envs(access_token=request.cookies['auto_report_wp'])['environments']
    envs = [{'name':i['name']} for i in envs]
    vms = apis.get_vms(access_token=request.cookies['auto_report_wp'])['vms']
    vms = [{'name':i['vm']} for i in vms if i['status']=='N']
    print(envs)
    test_suites = apis.get_test_suites(
    access_token=request.cookies['auto_report_wp'])['test_suites']
    test_suites = [{'name':i['name'].split(".")[0]} for i in test_suites]
    # print(test_suites)
    return render_template("schedules.html",envs=envs,vms=vms,
    schedules=schedules['tasks'],test_suites=test_suites,fill_i=fill_i)


@app.route("/users",methods=['GET','POST'])
def users():
    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if not con["status"]:
            return redirect(url_for('login'))
        elif request.cookies['token_type'] != 'a':
            return render_template('noaccess.html')
    else:
        flash("Your session is expired")
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'do' in request.form:
            if request.form['do']=='add':
                data = {'users':[{i:request.form[i] for i in request.form if i!='do'}]}
                res = apis.add_user(request.cookies.get('auto_report_wp'),data=data)
                # print(res)
                flash(res[0]['remarks'])

        if "delete" in request.form:
            data = {"email":request.form['delete']}
            res = apis.delete_user(request.cookies.get('auto_report_wp'),data=data)
            flash(res["remarks"])
            # print(res)

    users = apis.get_users(access_token=request.cookies['auto_report_wp'])
    if 'users' in users:
        return render_template("users.html",
        users=users['users'])
    else:
        return "some problem {0}".format(str(users))

@app.route("/test suites",methods=['GET','POST'])
def test_suites():

    if request.method == 'GET':
        if 'auto_report_wp' in request.cookies:
            con = apis.validate_auth(request.cookies.get('auto_report_wp'))
            if not con["status"]:
                return redirect(url_for('login'))
            # elif request.cookies['token_type'] != 'a':
            #     return render_template('noaccess.html')

    elif request.method == 'POST':

            if 'do' in request.form:
                if request.form['do']=='add':
                    file = request.files['file']
                    # print(file.__doc__)
                    data = {"name":file.filename,"description":request.form['description'],
                    "status":"N","environment":None}
                    res = apis.add_test_suites(request.cookies.get('auto_report_wp'),data=data)

                    if res["status"]:
                        file_path = os.getcwd()+"/test_suites_ware_house/"
                        if not os.path.exists(file_path):
                            os.makedirs(file_path)
                        file.save(file_path+secure_filename(filename=file.filename))
                        files={"upload_file":open(file_path+"/"+secure_filename(filename=file.filename),"rb")}
                        ud_res = apis.upload_doc(request.cookies.get('auto_report_wp'),files=files)
                        # print(ud_res)
                        if ud_res["status"]:
                            flash(res["remarks"])
                            if os.path.exists(file_path+file.filename):
                                os.unlink(file_path+file.filename)
                        else:
                            data = {'test_suites':[file.filename]}
                            res = apis.delete_test_suites(request.cookies.get('auto_report_wp'),data=data)
                            flash("Some problem with the uploading files please contact support")
                    else:
                        flash(res["remarks"])

            if 'download' in request.form:
                d_s = apis.get_test_suites(request.cookies.get('auto_report_wp'))
                test_suites_l =[i['name'] for i in d_s['test_suites']]
                file_path = os.getcwd()+"/test_suites_ware_house/"
                if request.form['download'] in test_suites_l:
                    # return send_file(file_path+secure_filename(request.form['download']),
                    # attachment_filename=secure_filename(request.form['download']),
                    # as_attachment=True)
                    data = {'file':request.form['download']}
                    return apis.download_doc(request.cookies.get('auto_report_wp'),data=data)

            elif 'delete' in request.form:
                data = {'test_suites':[request.form["delete"]]}
                res = apis.delete_test_suites(request.cookies.get('auto_report_wp'),data=data)
                dc_res = apis.delete_doc(request.cookies.get('auto_report_wp'),data={"file":request.form["delete"]})
                # print("hey")
                file_path = os.getcwd()+"/test_suites_ware_house/"
                # print(file_path)
                # if os.path.exists(file_path+secure_filename(request.form['delete'])):
                #     # print(request.form['delete'])
                #     os.unlink(file_path+secure_filename(request.form['delete']))
                flash(res['remarks'])


    test_suites = apis.get_test_suites(
    access_token=request.cookies['auto_report_wp'])['test_suites']
    return render_template("test suites.html",
    test_suites=test_suites)


@app.route("/manage_vms",methods=['GET','POST'])
def manage_vms():

    if 'auto_report_wp' in request.cookies:
        con = apis.validate_auth(request.cookies.get('auto_report_wp'))
        if not con["status"]:
            return redirect(url_for('login'))
        elif request.cookies['token_type'] != 'a':
            return render_template('noaccess.html')
    else:
        flash("Your session is expired")
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'do' in request.form:
            if request.form['do'] == 'add':
                data = {"vms":[{i:request.form[i] for i in request.form if i!='do'}]}
                res = apis.add_vms(access_token=request.cookies['auto_report_wp'],data=data)
                flash(res[0]['remarks'])

        if 'delete' in request.form:
            data = {"vms":[request.form[i] for i in request.form]}
            res = apis.delete_vms(access_token=request.cookies['auto_report_wp'],data=data)
            flash(res[0]['remarks'])

    vms = apis.get_vms(access_token=request.cookies['auto_report_wp'])['vms']
    return render_template("manage_vms.html",
    vms=vms)

@app.route("/login",methods=['POST'])
def logout():
    if 'auto_report_wp' in request.cookies:
        con = apis.logout(request.cookies.get('auto_report_wp'))
        if con["status"]:
            return render_template('login.html',text=con["remarks"])
        else:
            return render_template('login.html',text=con["remarks"])

@app.route("/execute suite",methods=['GET','POST'])
def execute():
    # print(request.form)
    if request.method == 'POST':
        file = request.files['file']
        file.save('uploaded '+file.filename)
    return render_template('execute.html')



if __name__=="__main__":
    pass
