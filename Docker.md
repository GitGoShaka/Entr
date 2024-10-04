- build package file for app: ``docker compose build``


Deploy image to docker 
- for each service:
    - Tag ``docker tag REPO:VERSION USERNAME/REPONAME/``
    - Push to repo: ``docker push 537124951786.dkr.ecr.eu-central-1.amazonaws.com/REPONAME``

]




Try later:
https://bentranz.medium.com/deploy-dockerized-application-to-aws-elastic-beanstalk-f8a3cf2944a7

- create repo for each service in AWS and get CLI access
- connect repo through: ``aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin YOURDOMAIN.dkr.ecr.eu-central-1.amazonaws.com``
- for each service:
    - Tag ``docker tag REPO:VERSION 537124951786.dkr.ecr.eu-central-1.amazonaws.com/REPONAME``
    - Push to repo: ``docker push 537124951786.dkr.ecr.eu-central-1.amazonaws.com/REPONAME``
Deploying app to aws:
``eb create --instance_type t2.micro --cname Entr --platform "Docker" --envvars POSTGRES_PASSWORD=your_db_password``


