"""
This module runs a simple Flask-based front-end to Babylon/Anarchy 
ResourceClaims
"""
import os
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap

# Check if we are running inside a Pod by checking this file
if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace"):
# current namespace thanks to Ralph: https://github.com/kubernetes-client/python/issues/363
    cr_namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
    config.load_incluster_config()
else:
# current namespace thanks to Ralph: https://github.com/kubernetes-client/python/issues/363
    config.load_kube_config()
    cr_namespace = config.list_kube_config_contexts()[1]['context']['namespace']

cr_group = 'poolboy.gpte.redhat.com'
cr_version = 'v1'
cr_plural = 'resourceclaims'
api = client.CustomObjectsApi()
cr_name = ''

body_start = {"spec":{"template":{"spec":{"desiredState": "started"}}}}
body_stop = {"spec":{"template":{"spec":{"desiredState": "stopped"}}}}

btn_classes = {
    'start':  ['btn', 'btn-success'],
    'stop':   ['btn', 'btn-primary'],
    'delete': ['btn', 'btn-danger'],
    'info':   ['btn', 'btn-info'],
}

app = Flask(__name__)
bootstrap = Bootstrap(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global cr_name
    try:
        response = api.list_namespaced_custom_object(cr_group,
                                                     cr_version,
                                                     cr_namespace,
                                                     cr_plural)
    except ApiException:
        return render_template('notfound.html')

    try:
        cr_name = response['items'][0]['metadata']['name']
    except IndexError:
        return render_template('notfound.html')


    cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                 cr_namespace, cr_plural,
                                                 cr_name)

    if (cr_status['spec']['template']['spec']['desiredState'] == 'stopped' and
            len(btn_classes['stop']) < 3):
        btn_classes['stop'].append('disabled')

    if (cr_status['spec']['template']['spec']['desiredState'] == 'started' and
            len(btn_classes['start']) < 3):
        btn_classes['start'].append('disabled')

    try:
        curr_state = cr_status['status']['resource']['status']['state']
    except KeyError:
        return render_template('starting.html')


    if (cr_status['status']['resource']['status']['state'] == 'stopped' and 
        cr_status['spec']['template']['spec']['desiredState'] == 'stopped' and
        len(btn_classes['start']) >= 3):
        btn_classes['start'].pop(-1)

    if (cr_status['status']['resource']['status']['state'] == 'started' and
        cr_status['spec']['template']['spec']['desiredState'] == 'started' and
        len(btn_classes['stop']) >= 3):
        btn_classes['stop'].pop(-1)

    
    return render_template('index.html', 
                           btn_classes=btn_classes,
                           cr_status=cr_status)

@app.route('/version')
def version():
    return os.getenv("VERSION", "0.0")

@app.route('/start')
def start():
    cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                 cr_namespace, cr_plural,
                                                 cr_name)
# Disable Start and enable Stop buttons
    if len(btn_classes['start']) < 3:
        btn_classes['start'].append('disabled')
    if len(btn_classes['stop']) >= 3:
        btn_classes['stop'].pop(-1)
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
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                 cr_namespace, cr_plural,
                                                 cr_name)
# Disable Stop and enable Start buttons
    if len(btn_classes['stop']) < 3:
        btn_classes['stop'].append('disabled')
    if len(btn_classes['start']) >= 3:
        btn_classes['start'].pop(-1)
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
    return redirect(url_for('index'))

@app.route('/delete')
def delete():
    cr_status = api.get_namespaced_custom_object(cr_group, cr_version,
                                                 cr_namespace, cr_plural,
                                                 cr_name)
    body = client.V1DeleteOptions()
    try:
        response = api.delete_namespaced_custom_object(
            group=cr_group,
            version=cr_version,
            plural=cr_plural,
            name=cr_name,
            namespace=cr_namespace,
            body=body)
    except ApiException as e:
        print("Exception when calling \
              CustomObjectsApi->patch_namespaced_custom_object: %s\n" % e)
    return redirect(url_for('index'))

