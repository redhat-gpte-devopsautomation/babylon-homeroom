from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from app.forms import ResourceForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ResourceForm()
    return render_template('index.hmtl', form=form)

@app.route("/version")
def version():
    return os.getenv("VERSION", "0.0")

@app.route("/start")
def start():
    try:
        response = api.patch_namespaced_custom_object(
            group=cr_group,
            version=cr_version,
            plural=cr_plural,
            name=cr_name, 
            namespace=cr_namespace, 
            body=body_start)
    except ApiException as e:
        print("Exception when calling \
              CustomObjectsApi->patch_namespaced_custom_object: %s\n" % e)
    return "STARTED"

@app.route("/stop")
def stop():
    try:
        response = api.patch_namespaced_custom_object(
            group=cr_group,
            version=cr_version,
            plural=cr_plural,
            name=cr_name, 
            namespace=cr_namespace, 
            body=body_stop)
    except ApiException as e:
        print("Exception when calling \
              CustomObjectsApi->patch_namespaced_custom_object: %s\n" % e)
    return "STOPPED"
