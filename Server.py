import Global
from User import User
from flask import Flask, request, flash, render_template, redirect
from flask_login import LoginManager, UserMixin, \
                        login_user, login_required, \
                        logout_user, current_user, AnonymousUserMixin

from Assignment import Assignment
from Assignment import StudentFile
from Assignment import Testcase

# initialize:
# flask, flask-login manager
app = Flask(__name__)
loginManager = LoginManager()
loginManager.init_app(app)
app.secret_key = "some key"


# utility functions
def flaskout(*args, **kwargs):
    print(*args, **kwargs)


def _getUsrPswd(form):
    return form.get("username"), form.get("password")


# main site: server status
@app.route('/')
def main():
    if current_user.is_authenticated:
        return redirect("/Dashboard/", code=302)
    return render_template('index.htm')


@app.route('/login/')
def login(errorMsg=None):
    if current_user.is_authenticated:
        return redirect("/Dashboard/", code=302)
    return render_template('login.htm', error=errorMsg)


@app.route('/login/action/', methods=['POST'])
def login_action():
    ''' flask login user '''
    username, inpswd = _getUsrPswd(request.form)
    # check user validity
    user = None
    if User.usr_pswd.hasUser((username, inpswd)):
        user = User.fromLogin(username, inpswd)
        flaskout("server.login:", user.id, "logged in")
        flaskout("User dict:", user.__dict__)
    else:
        return login(f"({username}, {inpswd}) is Not valid")
 
    login_user(user)
    flaskout("current user:", current_user)
    flaskout("current_user.__dict__: ", current_user.__dict__)
    return redirect("/", code=302)


# Web Interfaces
@loginManager.user_loader
def load_user(userid):
    """ returns current user """
    if User.usr_pswd.hasUsername(userid):
        serial = User.usr_pswd.getSerialByName(userid)
        usr = User.mangoLoad(serial)
        return usr
    else:
        return None


@app.route('/register/')
def register(errorMsg=None):
    if current_user.is_authenticated:
        return redirect("/Dashboard/", code=302)
    return render_template('register.htm', error=errorMsg)


@app.route('/register/action/', methods=['POST'])
def register_action():
    username, password = _getUsrPswd(request.form)
#     # case 1
#     if User.usr_pswd.hasUser((username, password)):
#         return f"You ({username},{password}) already have an account!"
    # case 2
    if User.usr_pswd.hasUsername(username):
        return register(f"username {username} in use")
    # case 3
    usr = User.newUser(username, password)
    flaskout("flask.register: new user")
    flaskout(f"username = {username}, password = {password}, "
             f"serial = {usr.serial} (debug)")
    login_user(usr)
    return redirect("/", code=302)


@app.route('/Dashboard/')
@login_required
def dashBoard(error = None):
    ds = {"username": current_user.id,
          "asmts": [],
          "error": error
    }
    for asmtSerial in current_user.asmtList:
        asmt = Assignment.mangoLoad(int(asmtSerial))
        ds["asmts"].append((asmt.asmtName, str(asmtSerial)))

    # use ds as your data structure
    return render_template('dashboard.htm', para=ds)


@app.route('/asmt/<serialNumber>/')
@login_required
def loadAsmtPage(serialNumber):
    
    asmt = Assignment.mangoLoad(int(serialNumber))
    # use asmt here, which is loaded
    #
    alltest = []
    for test_serial in asmt.getResult(current_user.id)[1]:
        alltest.append(Testcase.mangoLoad(test_serial))

    funcs = {}
    for test in alltest:
        funcs.setdefault(test.getName(), [])
        funcs[test.getName()].append(test.serial)

    ds = {
        "username" : current_user.id,
        "stuCode" : asmt.getPrevSub(current_user.id),
        "funcs" : funcs,
        "asmtname": asmt.asmtName,
        'serialNumber': asmt.serial
    }
    return render_template('assignment.htm', para=ds)
    

@app.route('/asmt/<asmtSerial>/upload/', methods=['POST'])
@login_required
def upload(asmtSerial):
    flaskout("server.upload: started")
    studentCode = request.files.get('studentCode')
    flaskout(current_user, current_user.__dict__)
    flaskout("server.upload: finished")
    studentCodeStr = studentCode.read().decode("utf-8")
    flaskout("file contents:", studentCodeStr)
    flaskout("file contents finished")
    asmt = Assignment.mangoLoad(int(asmtSerial))
    asmt.upload(current_user.id, studentCodeStr)
    asmt.mangoSave()
    return redirect(f"/asmt/{asmtSerial}/")

# 
# # error handlers
# @loginManager.unauthorized_handler
# def unauthorized():
#     flaskout(User.usr_pswd.usr_pswd)
#     flaskout(current_user, "tried to access unauthorized page")
#     return "handled unauthorized page"
# 
# @app.errorhandler(404)
# def page_not_found(e):
#     flaskout(current_user, "accessed page that does not exist")
#     # note that we set the 404 status explicitly
#     return "404"

@app.route('/addasmt/')
@login_required
def addAsmt():
    """ user add asmt using get request """
    asmtSerial = request.args.get('serial')
    try:
        if type(Assignment.mangoLoad(int(asmtSerial))) != Assignment:
            return dashBoard(f"Assignment {asmtSerial} is Not valid")
    except:
        return dashBoard(f"Assignment {asmtSerial} is Not valid")
    flaskout(f"{current_user} tried to add asmt: {asmtSerial}")
    current_user.asmtList.append(asmtSerial)
    current_user.mangoUpdate()
    return redirect("/Dashboard/", code=302)

@app.route('/debug/addAsmt')
def debugAddAsmt():
    """ debug force add asmt """
    assigner = request.args.get("assigner")
    asmtName = request.args.get("asmtName")
    newasmt = Assignment(assigner, asmtName)
    newasmt.serial = Global.NEXT_SERIAL
    newasmt.mangoSave()
    return f"added: Assignment({newasmt.serial}, {assigner}, {asmtName}) to database"

@app.route('/logout/')
@login_required
def logout():
    '''logout current user'''
    flaskout(current_user, ":", current_user.__dict__)
    flaskout("tried to logout")

    res = None
    if current_user.is_authenticated:
        userid = current_user.get_id()
        logout_user()
        res = f"{userid} logged out"
        flaskout(res)
        flaskout("succeeded")
        return redirect('/', code=302)


if __name__ == "__main__":

    app.config['SESSION_TYPE'] = 'mongodb'
    app.run(host=Global.SERVER_HOST, port=Global.SERVER_PORT, debug=True)

# http://127.0.0.1:7777/WeTest
