FROM  python:3

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY web3-redis.py ./

RUN pip3 install gevent redis

COPY . .

EXPOSE 8080
CMD [ "python3", "web3-redis.py" ]

# docker build -t irrlab/webpycache:1.0.0 .
# http -v http://ECS-first-run-alb-2072252323.us-east-1.elb.amazonaws.com:8080/
# aws ecr get-login --no-include-email
# aws ecr describe-repositories
# aws ecr create-repository --repository-name webcache
# docker tag irrlab/webpycache:1.0.0 041936244769.dkr.ecr.us-east-1.amazonaws.com/webpycache:1.0.0
# docker push 041936244769.dkr.ecr.us-east-1.amazonaws.com/webpycache:1.0.0
# aws ecr describe-images --repository-name webpycache
# aws ecr batch-delete-image --repository-name webpycache --image-ids imageTag=1.0.0
# aws ecr delete-repository --repository-name webpycache --force
# docker logout
