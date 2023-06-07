from oauthenticator.generic import GenericOAuthenticator
# subclassing the GenericOAuthenticator in case we need to 
# enrich the user info
# https://github.com/jupyterhub/oauthenticator/blob/main/oauthenticator/generic.py

class KeycloakAuthenticator(GenericOAuthenticator):
    login_service = 'keycloak'
    userdata_params = {"state": "state"}
    username_key =  "preferred_username"
    admin_groups = ["jupyterhub-admin"]
    allowed_groups = ["jupyterhub-user", "jupyterhub-admin"]
    enable_auth_state =  True

    def claim_groups_key(self, userinfo_data):
        return userinfo_data['jupyterhub_groups']

    
