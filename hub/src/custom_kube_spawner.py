import json
from kubespawner import KubeSpawner


class CustomKubeSpawner(KubeSpawner):
    def auth_state_hook(self, spawner, auth_state):
        """
        This user hook attaches the user information to the spawner,
        which we can use when generating the profile list.
        This allows us to have kubernetes overrides base on OAuth2 attributes.
        """
        userinfo = auth_state.get("oauth_user")
        self.log.info(f"got user info {userinfo}")
        spawner.userinfo = userinfo

    def profile_list(self, spawner):
        """
        The profile list for the KubeSpawner can be a callable from the Spawner object
        Allowing us to dynamically generate profiles based on the user info
        """
        user_info = spawner.userinfo
        image_options = {"display_name": "Image", "choices": {"pytorch": {"display_name": "Python 3 Training Notebook 1", "kubespawner_override": {"image": "training/python:2022.01.01"} } , "pytorch2": {"display_name": "Python 3 Training Notebook 2", "kubespawner_override": {"image": "training/python:2022.01.01"} } }}
        return [{'display_name': f'Training Env for {user_info.get("name")}', 'slug': 'training-python', 'default': True, "profile_options": {"image": image_options} }, {'display_name': f'Prod Env for {user_info.get("name")}','slug': 'prod-python','default': False}]

    def get_env(self):
        env = super().get_env()
        if hasattr(self,'userinfo'):
            env['PROP_USER_INFO'] = self.userinfo.get("name", "")
        if hasattr(self, 'user_options'):
            env['PROP_USER_PROFILE'] = self.user_options.get("profile","")
        self.log.info(f"Got environment variables {env}")
        return env