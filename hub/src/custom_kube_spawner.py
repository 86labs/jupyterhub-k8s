import json
from kubespawner import KubeSpawner
from kubernetes_asyncio.client import models as k8s

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
        image_options = {"display_name": "Image", "choices": {"custom": {"display_name": "Custom Single Server", "kubespawner_override": {"image": "gfeldman8/jupyterhub-k8s-singleuser:latest"} } , "pytorch2": {"display_name": "Python 3 Training Notebook 2", "kubespawner_override": {"image": "training/python:2022.01.01"} } }}
        return [{'display_name': f'Training Env for {user_info.get("name")}', 'slug': 'training-python', 'default': True, "profile_options": {"image": image_options} }, {'display_name': f'Prod Env for {user_info.get("name")}','slug': 'prod-python','default': False}]

    def get_env(self):
        env = super().get_env()
        if hasattr(self,'userinfo'):
            env['PROP_USER_INFO'] = self.userinfo.get("name", "")
        if hasattr(self, 'user_options'):
            env['PROP_USER_PROFILE'] = self.user_options.get("profile","")
        self.log.info(f"Got environment variables {env}")
        return env
    
    def get_service_account_from_user_info(self, spawner):
        user_info = spawner.userinfo
        self.log.info(f"got user info in modify_pod_hook {user_info}")
        return "jupyterhub-user"
    
    def modify_pod_hook(self, spawner, pod: k8s.V1Pod):
        # set service account based on user info
        pod.spec.service_account = self.get_service_account_from_user_info(spawner)
        pod.spec.service_account_name = self.get_service_account_from_user_info(spawner)
        pod.spec.automount_service_account_token = True
        # set user root to read only file system so they do not store files there permanently
        pod.spec.volumes.append(k8s.V1Volume(name="jupyter-root",empty_dir=k8s.V1EmptyDirVolumeSource()))
        pod.spec.containers[0].volume_mounts.append(k8s.V1VolumeMount(name="jupyter-root", mount_path="/tmp/container",read_only=False))
        pod.spec.containers[0].image_pull_policy = "Always"
        self.log.info(f"got pod in modify_pod_hook {pod}")
        return pod