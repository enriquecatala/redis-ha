<div>
    <a href="https://github.com/sponsors/enriquecatala"><img src="https://img.shields.io/badge/GitHub_Sponsors--_.svg?style=flat-square&logo=github&logoColor=EA4AAA" alt="GitHub Sponsors"></a>
    <a href="https://enriquecatala.com"><img src="https://img.shields.io/website?down_color=red&down_message=down&label=enriquecatala.com&up_color=46C018&url=https%3A%2F%2Fenriquecatala.com&style=flat-square" alt="Data Engineering with Enrique Catalá"></a>
    <a href="https://www.linkedin.com/in/enriquecatala"><img src="https://img.shields.io/badge/LinkedIn--_.svg?style=flat-square&logo=linkedin" alt="LinkedIn Enrique Catalá Bañuls"></a>
    <a href="https://twitter.com/enriquecatala"><img src="https://img.shields.io/twitter/follow/enriquecatala?color=blue&label=twitter&style=flat-square" alt="Twitter @enriquecatala"></a>
    <a href="https://youtube.com/enriquecatala"><img src="https://raw.githubusercontent.com/enriquecatala/enriquecatala/master/img/youtube.png" alt="Data Engineering: Canal youtube de Enrique Catalá" height=20></a>
</div>

<a href="https://mvp.microsoft.com/es-es/PublicProfile/5000312?fullName=Enrique%20Catala"><img src="https://raw.githubusercontent.com/enriquecatala/enriquecatala/master/img/MVP_Logo_horizontal.png" alt="Microsoft DataPlatform MVP Enrique Catalá"></a>

- [Redis](#redis)
  - [Configurations:](#configurations)
- [Deployment](#deployment)
  - [Add AKS nodepool](#add-aks-nodepool)
  - [Create namespace and secret](#create-namespace-and-secret)
  - [Deploy helm](#deploy-helm)
  - [Option 1) Deploy with taints and tolerations (PREFERED)](#option-1-deploy-with-taints-and-tolerations-prefered)
  - [Option 2) Deploy redis without tolerations and without yaml file](#option-2-deploy-redis-without-tolerations-and-without-yaml-file)
  - [Test](#test)
    - [Option1) Test from container](#option1-test-from-container)
    - [Option2) Test from local machine](#option2-test-from-local-machine)
    - [Expected output](#expected-output)
    - [Uninstall chart](#uninstall-chart)
      - [Delete all data](#delete-all-data)
# Redis

This document will help you to deploy redis in AKS on a sentinel-master-slave architecture with spot instances and dedicated nodepool.

For complete documentation: https://github.com/bitnami/charts/tree/master/bitnami/redis

```bash
# get values.yaml
 curl -Lo values.yaml https://raw.githubusercontent.com/bitnami/charts/master/bitnami/redis/values.yaml
 ```

 ## Configurations:

  - master-slave with sentinel
    - sentinel.enabled = true
    - architecture=replication
 - Password from secret
    - usePasswordFile=true
    - existingSecret=redis-password-secret
    - sentinels.enabled=true
    - metrics.enabled=true
  - appendonly yes
    - From now on, every time Redis receives a command that changes the dataset (e.g. SET) it will append it to the AOF. When you restart Redis it will re-play the AOF to rebuild the state.



To create the secret from password:

```bash
kubectl create secret generic my-redis-secret --from-literal=redis-password=somesecretpassword
```

<mark>Important</mark> the filename must be `redis-password.yaml` For more info: https://docs.bitnami.com/kubernetes/infrastructure/redis/administration/use-password-file/

# Deployment

## Add AKS nodepool

```bash
## delete old nodepool (optional)
#
# az aks nodepool delete --cluster-name sentinelaksdemo \
#                       --resource-group ES-ITCO-TECHL-01-IS-ADM-NC-STD-XXX \
#                       --name redis
    

## add new nodepool (Spot dedicated to redis)
#
az aks nodepool add --cluster-name sentinelaksdemo \
                    --resource-group ES-ITCO-TECHL-01-IS-ADM-NC-STD-XXX \
                    --name redis \
                    --enable-cluster-autoscaler \
                    --eviction-policy Delete \
                    --max-count 4 \
                    --min-count 3 \
                    --priority Spot \
                    --node-taints "dedicated=redis:NoSchedule" \
                    --node-vm-size Standard_E4s_v3	# 32Gb of ram
```

## Create namespace and secret
```
kubectl create namespace redis

kubectl create secret generic my-redis-secret \
      --from-literal=redis-password=somesecretpassword \
      --namespace redis

```
## Deploy helm

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Option 1) Deploy with taints and tolerations (PREFERED)

```
helm install redis bitnami/redis \
  -f redis-values-production.yaml \
  --create-namespace \
  --namespace redis
```

>NOTE: For more info: https://github.com/bitnami/charts/tree/master/bitnami/redis

## Option 2) Deploy redis without tolerations and without yaml file
 It takes ~5 minutes to deploy the chart
 By default it deploys with PVC to azure-disk and reclaim-policy=Delete (but helm uninstall redis does NOT delete the PVC, so data will be preserved)
  kubectl get pvc, pv

```
helm install redis bitnami/redis \
  --set architecture=replication \
  --set sentinel.enabled=true \
  --set auth.enabled=true \
  --set auth.usePasswordFiles=true \
  --set auth.existingSecret=my-redis-secret \
  --set auth.existingSecretPasswordKey=redis-password \
  --create-namespace \
  --namespace redis
```
## Test

### Option1) Test from container
```
export REDIS_PASSWORD=$(kubectl get secret --namespace redis my-redis-secret -o jsonpath="{.data.redis-password}" | base64 --decode)
kubectl run redis-client --restart='Never' --rm --env REDISCLI_AUTH=$REDIS_PASSWORD  --image docker.io/bitnami/redis:6.2.6-debian-10-r53  --namespace redis -it  -- /bin/bash 

# now, inside the container
REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis -p 6379 # Read only operations
REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis -p 26379 # Sentinel access

# to get the master node (readwrite) FROM SENTINEL
SENTINEL get-master-addr-by-name mymaster

```
### Option2) Test from local machine

``` 
export REDIS_PASSWORD=$(kubectl get secret --namespace redis my-redis-secret -o jsonpath="{.data.redis-password}" | base64 --decode)

# Open port-forwarding 
kubectl port-forward --namespace redis svc/redis 6379:6379 

# Load all data
cat /mnt/d/Clientes/SentinelML/prepared_blacklist_for_redis/part-00000-tid-8877533473703218517-d3e24d59-c5ee-4a52-9c37-9b89a217b070-263-1-c000.csv | redis-cli -h 127.0.0.1 -p 6379 -a somesecretpassword --pipe

```


### Expected output

```bash
NAME: redis
LAST DEPLOYED: Tue Dec 14 12:43:35 2021
NAMESPACE: redis
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: redis
CHART VERSION: 15.6.4
APP VERSION: 6.2.6

** Please be patient while the chart is being deployed **

Redis&trade; can be accessed via port 6379 on the following DNS name from within your cluster:

    redis.redis.svc.cluster.local for read only operations

For read/write operations, first access the Redis&trade; Sentinel cluster, which is available in port 26379 using the same domain name above.



To get your password run:

    export REDIS_PASSWORD=$(kubectl get secret --namespace redis my-redis-secret -o jsonpath="{.data.redis-password}" | base64 --decode)

To connect to your Redis&trade; server:

1. Run a Redis&trade; pod that you can use as a client:

   kubectl run --namespace redis redis-client --restart='Never'  --env REDISCLI_AUTH=$REDIS_PASSWORD  --image docker.io/bitnami/redis:6.2.6-debian-10-r53 --command -- sleep infinity

   Use the following command to attach to the pod:

   kubectl exec --tty -i redis-client \
   --namespace redis -- bash

2. Connect using the Redis&trade; CLI:
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis -p 6379 # Read only operations
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis -p 26379 # Sentinel access

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace redis svc/redis 6379:6379 &
    REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h 127.0.0.1 -p 6379
```

### Uninstall chart

```
# Data will NOT be destroyed
# This will clean pods, services,configmaps...but not secrets
helm uninstall  redis --namespace redis
```

#### Delete all data

<mark>THIS WILL DESTROY ALL YOUR DATA</mark> since the PVC is reclaim-policy=Delete
```
kubectl -n redis delete pvc redis-data-redis-node-0
kubectl -n redis delete pvc redis-data-redis-node-1
kubectl -n redis delete pvc redis-data-redis-node-2
```