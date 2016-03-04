#!/usr/bin/python
import flask
import json
import re
import random
import string
import os
import hashlib

from DBConsumer import DBConsumer
from MoneoChecker import MoneoChecker

app = flask.Flask(__name__)

class AuthError(BaseException):
    pass

class ValidationError(BaseException):
    pass

def get_post_param(param, default="", mandatory=False):
    res = default
    if param in flask.request.form:
        if mandatory and param.strip() == "":
            raise ValidationError('Parameter "%s" must not be empty' % param)
        res = flask.request.form[param]
    elif mandatory:
        raise ValidationError('Parameter "%s" is mandatory' % param)
    return res

def test_logged():
    if "user" not in flask.session:
        raise AuthError("You are not logged")

@app.route("/is_logged")
def www_is_logged():
    res = False
    try:
        test_logged()
        res = True
    except AuthError:
        pass
    return json.dumps(res)

@app.route("/logout")
def www_logout():
    flask.session.pop("user", None)
    res = True
    return json.dumps(res)

@app.route("/login", methods=["POST"])
def www_login():
    res = False
    try:
        login = get_post_param("login", mandatory=True)
        password = get_post_param("password", mandatory=True)
        password = get_password(password)
        req = "SELECT password FROM user WHERE username = ?"
        row = DBConsumer.get_instance().query(req, (login,))
        if not row:
            raise AuthError("Erreur d'authentification")
        if row[0]['password'] != password:
            raise AuthError("Erreur d'authentification.")
        flask.session["user"] = login
        res = True
    except AuthError as ex:
        flask.abort(flask.make_response(str(ex), 403))
    except ValidationError as ex:
        flask.abort(flask.make_response(str(ex), 400))
    return json.dumps(res)

@app.route("/get_balances")
def www_get_balances():
    res = []
    try:
        test_logged()
        req = "SELECT (amount / 100.00) as amount, validity FROM balance WHERE amount > 0 ORDER BY validity"
        for row in DBConsumer.get_instance().query(req):
            res.append(dict(zip(row.keys(), row)))
    except AuthError as ex:
        flask.abort(flask.make_response(str(ex), 403))
    return json.dumps(res)

@app.route("/get_transactions")
def www_get_transactions():
    res = []
    try:
        test_logged()
        req = "SELECT name, (amount / 100.00) as amount, dt FROM transact ORDER BY dt DESC LIMIT 50"
        for row in DBConsumer.get_instance().query(req):
            res.append(dict(zip(row.keys(), row)))
    except AuthError as ex:
        flask.abort(flask.make_response(str(ex), 403))
    return json.dumps(res)

def get_password(raw_password):
    #TODO improve security of the password encryption
    return hashlib.sha1(raw_password).hexdigest()

def generate_random_secret(length):
    """
    Generate a random secret key to use with session.

    WARNING : maybe it is not strong enought, if you want to improv it your welcome !
    @param length the secret length
    @return (String) a secret key
    """
    chars = string.printable
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in xrange(length))

if __name__ == "__main__":
    conf = {}
    with open("moneoresto-checker.conf", "r") as fd:
        conf = json.load(fd)

    DBConsumer.get_instance()
    checker = MoneoChecker(conf["checker"])
    checker.start()
    try:
        # set the secret key.  keep this really secret:
        app.secret_key = generate_random_secret(1024)

        #TODO improve port (conf file ?)
        app.debug = False
        app.run(port=5123)
    finally:
        checker.stop()
        DBConsumer.get_instance().close()
