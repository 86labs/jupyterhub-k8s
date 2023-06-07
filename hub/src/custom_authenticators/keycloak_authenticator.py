import json

from oauthenticator.generic import GenericOAuthenticator
# subclassing the GenericOAuthenticator in case we need to 
# enrich the user info
# https://github.com/jupyterhub/oauthenticator/blob/main/oauthenticator/generic.py

class KeycloakAuthenticator(GenericOAuthenticator):
    pass
