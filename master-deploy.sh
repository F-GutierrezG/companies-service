# !/bin/bash
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker login -u gitlab-ci-token -p $DOCKER_TOKEN registry.gitlab.com"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network create --subnet=172.21.0.0/16 companies-service-network'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop companies'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container stop companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm companies'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container rm companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/companies-service/companies-swagger -q)'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/companies-service/companies -q)'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run -d --restart always -e 'API_URL=definitions/swagger.yml' --name companies-swagger --network companies-service-network --ip 172.21.0.3 $REGISTRY_REPO/$SWAGGER:$TAG"
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} "docker run -d --restart always -e 'FLASK_ENV=production' -e 'FLASK_APP=manage.py' -e 'APP_SETTINGS=project.config.ProductionConfig' -e 'DATABASE_URL=postgres://$DATABASE_PROD_USER:$DATABASE_PROD_PASSWORD@$DATABASE_PROD_URL:$DATABASE_PROD_PORT/$DATABASE_PROD_NAME' -e 'SECRET_KEY=$PROD_SECRET_KEY' -e USERS_SERVICE_URL=$USERS_SERVICE_URL -e AUTH_SERVICE_URL=$AUTH_SERVICE_URL --name companies --network companies-service-network --ip 172.21.0.2 $REGISTRY_REPO/$COMPANIES:$TAG"

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.8 companies'
ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker network connect onelike-network --ip 172.18.0.9 companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${PRODUCTION_SERVER} 'docker container exec companies python manage.py db upgrade'
