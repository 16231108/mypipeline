kubectl apply -k "manifests/kustomize/cluster-scoped-resources"
kubectl apply -k "manifests/kustomize/env/platform-agnostic-pns"
sodu service docker start
minikube start
kubectl get pods -n kubeflow
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8082:80
dsl-compile --py ${DIR}/lll.py --output ${DIR}/lll.tar.gz