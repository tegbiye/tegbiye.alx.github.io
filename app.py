from flask import Flask, render_template,session,redirect,json,jsonify
import re
from flask.globals import request

from DB_handler import *
app = Flask(__name__)
app.config.from_object("config")
app.secret_key='try_again'
dbHandler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])

@app.route('/')
def start():
    session.clear()
    return render_template("index.html")

@app.route('/signInPage')
def signInPage():
    session.clear()
    return render_template("login.html")
@app.route('/joinAsClient')
def clintSingUpPage():
    return render_template("newuser.html")
@app.route('/joinAsWorker')
def workerSingUpPage():
    return render_template("newaccount.html")
@app.route('/adminPage')
def adminPage():
    if session.get('loggedin')=='admin':
        return render_template("admin.html")
    return redirect('/signInPage')
@app.route('/dashboardPage')
def dashboardPage():
    if session.get('loggedin')=='client':
        saveSearch = dbHandler.getjobs()
        if saveSearch == []:
            return render_template("dashboard.html", Error="Currently no worker availble")
        else:
            return render_template("dashboard.html", jobList=saveSearch)
    return redirect('/signInPage')
@app.route('/searchresult', methods=['POST','GET'])
def searchedResults():
    if session.get('loggedin')=='client':
        saveSearch = dbHandler.getSearchedjobs(request.form['searchText'])
        if saveSearch == []:
            return render_template("dashboard.html", Error="Currently no worker availble")
        else:
            return render_template("dashboard.html", jobList=saveSearch)
    return redirect('/signInPage')
@app.route('/workerPage')
def workerPage():
    if session.get('loggedin')=='worker':
        return render_template("worker.html")
    return redirect('/signInPage')
@app.route('/clientPage')
def clientPage():
    if session.get('loggedin')=='client':
        return render_template("client.html")
    elif session.get('loggedin')=='admin':
        return render_template("admin.html")
@app.route('/user', methods=['POST','GET'])
def user():
    validation = dbHandler.validation(request.form['status'],request.form['email'],request.form['password'])
    if validation:
        session['id']=validation
        print(request.form['status'])
        if request.form['status']=="As Client":
            print(dbHandler.isAdmin(request.form['email']))
            if dbHandler.isAdmin(request.form['email']):
                session['loggedin']='admin'
                session['email']=request.form['email']
                return redirect('/adminPage')
            else:
                session['loggedin']='client'
                session['email']=request.form['email']
                return redirect('/dashboardPage')
        elif request.form['status']=="As Worker":
            session['loggedin']='worker'
            session['email']=request.form['email']
            return redirect('/workerPage')
    else:
        return render_template("/login.html",fail='Invalid credentials')
@app.route('/addNewClient',methods=['POST','GET'])
def addNewClient():
    if dbHandler.insertClient(request.form['name'],request.form['mobile'],request.form['city'],request.form['email'],request.form['password']):
        return render_template('/login.html',success='Registration done successfully,now get log In')
    else:
        if dbHandler.isClinetExist(request.form['email']):
           return render_template("/newaccount.html",fail='A account with this email already exist')
        else:
           return render_template("/newaccount.html",fail='Invalid details')
@app.route('/updateClientInfo',methods=['POST','GET'])
def updateClient():
    if dbHandler.updateClient(dbHandler.getClientId(session['email']),request.form['name'],request.form['mobile'],request.form['city'],request.form['email'],request.form['password']):
        return render_template('/client.html',success='Profile Update Successfully')
    else:
        return render_template('/client.html',fail='Invalid details')
@app.route('/addNewWorker', methods=['POST','GET'])
def addNewWorker():
   if dbHandler.insertWorker(request.form['name'],request.form['mobile'],request.form['title'],request.form['city'],request.form['email'],request.form['password']):
        return render_template('/login.html',success='Registration done successfully,now get log In')
   else:
        if dbHandler.isWorkerExist(request.form['email']):
           return render_template("/newaccount.html",fail='A account with this email already exist')
        else:
           return render_template("/newaccount.html",fail='Invalid details')
@app.route('/addNewJob',methods=['GET','POST'])
def addNewJob():
    if dbHandler.insertNewJob(dbHandler.getWorkerId(session['email']),request.form['title'],request.form['rate'],request.form['desc']):
        return render_template('/worker.html',success='Job Added')
    else:
        return render_template('/worker.html',fail='Request Denied')
@app.route('/logOut', methods=['POST','GET'])
def logItOut():
    session.clear()
    return redirect('/signInPage')

@app.route('/getInfo',methods=['GET'])
def getPersonDetails():
    print(session['loggedin'])
    if session['loggedin']=='worker':
        result= dbHandler.getWorkerInfo(session['email'])
        return json.dumps(result)
    elif session['loggedin']=='client' or session['loggedin']=='admin':
        result= dbHandler.getClientInfo(session['email'])
        return json.dumps(result)

@app.route('/jobDetails',methods=['GET','POST'])
def jobDetails():
    id=request.args.get('id')
    results=dbHandler.getJobDetails(id)
    return json.dumps(results)
@app.route('/sendHireRequest',methods=['GET','POST'])
def sendHiringRequest():
    cid=dbHandler.getClientId(session['email'])
    jid=request.form['jid']
    wid=request.form['wid']
    if dbHandler.sendRequest(jid,wid,cid):
        return redirect('/dashboardPage')
    else:
        return redirect('/dashboardPage')
@app.route('/requestData',methods=['GET'])
def getRequestedData():
    cid=dbHandler.getClientId(session['email'])
    results=dbHandler.getRequestedJobs(cid)
    return json.dumps(results)
@app.route('/confirmData',methods=['GET'])
def getAcceptedData():
    cid=dbHandler.getClientId(session['email'])
    results=dbHandler.getConfirmJobs(cid)
    return json.dumps(results)
@app.route('/requestDataForWorker',methods=['GET'])
def getRequestedDataForWorker():
    cid=dbHandler.getWorkerId(session['email'])
    results=dbHandler.checkRequestedJobs(cid)
    return json.dumps(results)
@app.route('/getMyJobs',methods=['GET'])
def getMyJobs():
    cid=dbHandler.getWorkerId(session['email'])
    results=dbHandler.checkMyJobs(cid)
    return json.dumps(results)
@app.route('/confirmDataForWorker',methods=['GET'])
def getConfirmDataForWorker():
    cid=dbHandler.getWorkerId(session['email'])
    results=dbHandler.checkConfirmJobs(cid)
    return json.dumps(results)
@app.route('/cancelRequest',methods=['POST'])
def cancelRequest():
    job_id=request.form['job_id']
    worker_id=request.form['worker_id']
    client_id=request.form['client_id']   
    if dbHandler.cancelRequest(worker_id,job_id,client_id):
        return json.dumps({"msg":"Canceled"})
    else:
        return json.dumps({"msg":"Can not Cancel"})
@app.route('/deleteMyJob',methods=['POST'])
def deleteMyJob():
    job_id=request.form['job_id']
    if dbHandler.deletejobP(job_id):
        return json.dumps({"msg":"Canceled"})
    else:
        return json.dumps({"msg":"Can not Cancel"})
@app.route('/closeTheJob',methods=['POST'])
def closeTheJob():
    job_id=request.form['job_id']
    worker_id=request.form['worker_id']
    client_id=request.form['client_id']
    ratings=request.form['star']
    if dbHandler.jobClose(worker_id,job_id,client_id,ratings):
        return json.dumps({"msg":"Job is closed"})
    else:
        return json.dumps({"msg":"Job is still in progress"})
@app.route('/acceptRequest',methods=['POST'])
def acceptRequest():
    job_id=request.form['job_id']
    worker_id=request.form['worker_id']
    client_id=request.form['client_id']   
    if dbHandler.acceptRequest(worker_id,job_id,client_id):
        return json.dumps({"msg":"Accepted"})
    else:
        return json.dumps({"msg":"Job is not confirmed"})
if __name__ == '__main__':
    app.run(debug=True)
