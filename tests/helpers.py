import flask
from flask import current_app
from flask_principal import Identity, identity_changed, AnonymousIdentity
from invenio_access import authenticated_user


def set_identity(u):
    """Sets identity in flask.g to the user."""
    if hasattr(u, 'id'):
        identity = Identity(u.id)
        identity.provides.add(authenticated_user)
        identity_changed.send(current_app._get_current_object(), identity=identity)
        assert flask.g.identity.id == u.id
    else:
        identity = AnonymousIdentity()
        identity_changed.send(current_app._get_current_object(), identity=identity)


def login(http_client, user):
    """Calls test login endpoint to log user."""
    resp = http_client.get(f'/test/login/{user.id}')
    assert resp.status_code == 200
