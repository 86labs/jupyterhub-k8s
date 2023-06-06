ARG JUPYTERHUB_TAG
FROM jupyterhub/k8s-hub:${JUPYTERHUB_TAG}

RUN mkdir -p /app/hub_custom
COPY src/custom_kube_spawner.py /app/hub_custom/custom_kube_spawner.py