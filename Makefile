export JUPYTERHUB_CHART_VERSION ?= "3.0.0-0.dev.git.6171.h0f4b2d0b"
export BASE_DEPLOYMENT = ./deploy/gke
export VALUES_FILE ?= ${BASE_DEPLOYMENT}/values.yaml
.PHONY: deploy render
repo:
	helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
	helm repo update
render:
	helm template jupyterhub \
			--namespace jupyterhub \
			--set-file hub.extraFiles.keycloak_authenticator.stringData=./hub/src/custom_authenticators/keycloak_authenticator.py \
			--set-file hub.extraFiles.custom_kube_spawner.stringData=./hub/src/custom_kube_spawner.py \
			--set-file singleuser.extraFiles.custom_content_manager.stringData=./singleuser/src/custom_content_manager.py \
			-f ${VALUES_FILE} \
			jupyterhub/jupyterhub \
			--version ${JUPYTERHUB_CHART_VERSION} > ${BASE_DEPLOYMENT}/helm_rendered.yaml

deploy: render
	kustomize build ${BASE_DEPLOYMENT} | kubectl apply -f -

destroy: render
	kustomize build ${BASE_DEPLOYMENT} | kubectl delete -f -