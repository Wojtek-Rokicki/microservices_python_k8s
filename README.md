# About the project
This project has educational purposes and it follows up the YT tutorial - [Microservice Architecture and System Design with Python & Kubernetes](https://www.youtube.com/watch?v=hmkF77F9TLw&list=PLoV7fSc2vRyOkvaIia2gqXKTYIX3evRRu&index=3&ab_channel=freeCodeCamp.org)
# Notes
## Process of designing the system
- set a goal of the project (conversion of the movie into mp3 file)
- draw a diagram (microservices, their communication, storages and workflow)
- structure the code into modules/folders
- define required tools and libraries
- setup the environment - install required software
- start implementing services

# Running the Application:
Before running application please set up MySQL and MongoDB databases. For MySQL run **init.sql** from auth folder and change email for existing one to receive the emails. 
```shell
kubectl apply -f ./python/src/rabbit/manifests/
kubectl apply -f ./python/src/gateway/manifests/
```
In separate shell to enable accessing rabbitmq management console
```shell
minikube tunnel
```
Then you need to setup the Classic queues: video, mp3 via rabbitmq-manager.com. 

In /python/src/notification/manifests/secret.yml pass your gmail account credentials.

Then continue building k8s infrastructure:
```shell
kubectl apply -f ./python/src/auth/manifests/
kubectl apply -f ./python/src/converter/manifests/
kubectl apply -f ./python/src/notification/manifests/
```
You can view the progression with **k9s** shell console.

## End-to-end tests
```shell
curl -X POST http://mp3converter.com/login -u georgio@email.com:Admin123
curl -X POST -F 'file=@./<path_to_video>' -H 'Authorization: Bearer <token>' http://mp3converter.com/upload
curl --output mp3_download.mp3 -X GET -H 'Authorization: Bearer <token>' http://mp3converter.com/download?fid=<mp3_resource_fid>
```