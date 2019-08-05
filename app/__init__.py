from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from app.forms import ResourceForm
import os
import socket
from kubernetes import client, config
from kubernetes.client.rest import ApiException


# Check if we are running inside a Pod by checking this file
if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace"):
# current namespace thanks to Ralph: https://github.com/kubernetes-client/python/issues/363
    cr_namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
    config.load_incluster_config()
else:
# current namespace thanks to Ralph: https://github.com/kubernetes-client/python/issues/363
    config.load_kube_config()
    cr_namespace = config.list_kube_config_contexts()[1]['context']['namespace']

cr_group = 'gpte.redhat.com'
cr_version = 'v1'
cr_plural = 'resourceclaims'
api = client.CustomObjectsApi()
response = api.list_namespaced_custom_object(cr_group, cr_version, cr_namespace, cr_plural)
cr_name = response['items'][0]['metadata']['name']

body_start = {"spec":{"desiredState":"running"}}
body_stop = {"spec":{"desiredState":"stopped"}}

app = Flask(__name__)
bootstrap = Bootstrap(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                  cr_namespace, cr_plural,
                                                  cr_name)
    form = ResourceForm()
    if request.method == 'POST':
        result = request.form
        if 'btn_stop' in result.keys():
            stop()
        if 'btn_start' in result.keys():
            start()
        if 'btn_update' in result.keys():
            cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                  cr_namespace, cr_plural,
                                                  cr_name)
            
    return render_template('index.html', form=form, 
                               cr_status=cr_status)

@app.route('/version')
def version():
    return os.getenv("VERSION", "0.0")

@app.route('/start')
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

@app.route('/stop')
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
