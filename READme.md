[gold_price_project_README.txt](https://github.com/user-attachments/files/26347950/gold_price_project_README.txt)
GOLD PRICE ALERT SYSTEM (EKS + KUBERNETES + SNS)

===============================
PROJECT SETUP GUIDE (STEP BY STEP)
===============================

STEP 1: CREATE EKS CLUSTER
--------------------------------
eksctl create cluster \
  --name gold-cluster \
  --region us-east-1 \
  --nodegroup-name gold-nodes \
  --node-type t2.micro \
  --nodes 2

--------------------------------
STEP 2: FIX KUBECTL (IF ERROR)
--------------------------------
rm -f /usr/local/bin/kubectl             ## use Only If KUBECTL is not Working ###

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl
mv kubectl /usr/local/bin/

kubectl version --client

--------------------------------
STEP 3: CONFIGURE EKS
--------------------------------
aws eks update-kubeconfig --region us-east-1 --name gold-cluster
kubectl get nodes

--------------------------------
STEP 4: SET AWS REGION
--------------------------------
aws configure
(Enter region: us-east-1)

--------------------------------
STEP 5: ENABLE OIDC
--------------------------------
eksctl utils associate-iam-oidc-provider \
  --cluster gold-cluster \
  --region us-east-1 \
  --approve

--------------------------------
STEP 6: CREATE IAM POLICY
--------------------------------
aws iam create-policy \
  --policy-name gold-sns-policy \
  --policy-document file://sns-policy.json

--------------------------------
STEP 7: CREATE IAM SERVICE ACCOUNT
--------------------------------
eksctl create iamserviceaccount \
  --name gold-price-sa \
  --namespace default \
  --cluster gold-cluster \
  --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/gold-sns-policy \
  --region us-east-1 \
  --approve

--------------------------------
STEP 8: CREATE SECRET (API KEY)
--------------------------------
kubectl create secret generic goldapi-secret \
  --from-literal=api_key=YOUR_API_KEY

--------------------------------
STEP 9: DOCKER SETUP
--------------------------------
docker login               #### use Username And Access Token For Password

docker build -t <your-docker-username>/gold-price:latest .
docker push <your-docker-username>/gold-price:latest

--------------------------------
STEP 10: DEPLOY CRONJOB
--------------------------------
kubectl apply -f gold-app.yaml

--------------------------------
STEP 11: CHECK RESOURCES
--------------------------------
kubectl get pods
kubectl get cronjobs
kubectl get jobs

--------------------------------
STEP 12: SCALE NODES (IF NEEDED)         ### If POD Get In Pending State Check Node And Describe POD, USE BELOW COMMAND TO SCALE THE NODE GROUP #####
--------------------------------
eksctl scale nodegroup \
  --cluster gold-cluster \
  --name gold-nodes \
  --region us-east-1 \
  --nodes-min 2 \
  --nodes-max 4 \
  --nodes 3

--------------------------------
STEP 13: CLEAN PENDING PODS
--------------------------------
kubectl delete pod --all

--------------------------------
STEP 14: RUN JOB MANUALLY
--------------------------------
kubectl create job --from=cronjob/gold-price-cronjob test-job

--------------------------------
STEP 15: CREATE SNS TOPIC
--------------------------------
aws sns create-topic --name gold-price-alerts

--------------------------------
STEP 16: SUBSCRIBE EMAIL
--------------------------------
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:<ACCOUNT_ID>:gold-price-alerts \
  --protocol email \
  --notification-endpoint your-email@gmail.com

(Check email and confirm subscription)

--------------------------------
STEP 17: TEST SNS
--------------------------------
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:<ACCOUNT_ID>:gold-price-alerts \
  --message "Test Gold Price Alert"


################################################################# TO DELETE ALL THE THING WHICH ARE CREATED #################################################################
--------------------------------
STEP 18: TEST GOLD API
--------------------------------
curl https://www.goldapi.io/api/XAU/INR \
  -H "x-access-token: YOUR_API_KEY" \
  -H "Content-Type: application/json"

--------------------------------
STEP 19: CLEANUP RESOURCES
--------------------------------
kubectl delete cronjob gold-price-cronjob
kubectl delete jobs --all
kubectl delete pods --all
kubectl delete secret goldapi-secret

--------------------------------
STEP 20: DELETE IAM SERVICE ACCOUNT
--------------------------------
eksctl delete iamserviceaccount \
  --name gold-price-sa \
  --namespace default \
  --cluster gold-cluster \
  --region us-east-1

--------------------------------
STEP 21: DELETE SNS TOPIC
--------------------------------
aws sns delete-topic \
  --topic-arn arn:aws:sns:us-east-1:<ACCOUNT_ID>:gold-price-alerts

--------------------------------
STEP 22: DELETE EKS CLUSTER
--------------------------------
eksctl delete cluster \
  --name gold-cluster \
  --region us-east-1

===============================
PROJECT COMPLETE
===============================
This project demonstrates:
- Kubernetes CronJobs
- AWS EKS
- IAM Roles (IRSA)
- SNS Notifications
- API Integration
- Docker Deployment

