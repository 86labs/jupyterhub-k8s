ARG JUPYTERHUB_TAG
FROM jupyterhub/k8s-hub:${JUPYTERHUB_TAG}

USER root
RUN mkdir -p /app/hub_custom
COPY src/ /app/hub_custom/

USER ${NBUSER}