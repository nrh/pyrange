# -*- coding: utf-8 -*-

from pyrange import app
import pyrange.store


@app.route('/')
def status():
    store = pyrange.store.get_store()
    return store.status()


@app.route('/ns/', methods=['GET'])
def list_namespaces():
    return 'hi!'


@app.route('/ns/', methods=['PUT'])
def add_namespace():
    return 'hi!'


@app.route('/ns/<namespace>', methods=['GET'])
def get_namespace(namespace):
    return 'hi!'


@app.route('/ns/<namespace>', methods=['PUT'])
def update_namespace(namespace):
    return 'hi!'


@app.route('/ns/<namespace>/roles', methods=['GET'])
def list_roles(namespace):
    return 'hi!'


@app.route('/ns/<namespace>/roles', methods=['PUT'])
def add_role(namespace):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>', methods=['GET'])
def get_role(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>', methods=['PUT'])
def update_role(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>/members', methods=['GET'])
def get_role_members(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>/members', methods=['PUT'])
def update_role_members(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>/tags', methods=['GET'])
def get_role_tags(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/roles/<role>/tags', methods=['PUT'])
def update_role_tags(namespace, role):
    return 'hi!'


@app.route('/ns/<namespace>/tags', methods=['GET'])
def get_tags(namespace):
    return 'hi!'


# questionable?
@app.route('/ns/<namespace>/tags', methods=['PUT'])
def update_tags(namespace):
    return 'hi!'


@app.route('/ns/<namespace>/tags/<tag>', methods=['GET'])
def get_tag(namespace, tag):
    return 'hi!'


@app.route('/ns/<namespace>/tags/<tag>', methods=['PUT'])
def update_tag(namespace, tag):
    return 'hi!'


@app.route('/members/<member>', methods=['GET'])
def get_member(member):
    return 'hi!'


@app.route('/members/<member>/<attr>', methods=['GET'])
def get_member_attr(member, attr):
    return 'hi!'


@app.route('/range/', methods=['POST'])
def post_range():
    return 'hi!'
