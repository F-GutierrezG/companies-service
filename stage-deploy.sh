# !/bin/bash
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} "docker login -u gitlab-ci-token -p $DOCKER_TOKEN registry.gitlab.com"

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker network create --subnet=172.21.0.0/16 companies-service-network'

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container stop companies'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container stop companies-db'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container stop companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container rm companies'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container rm companies-db'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container rm companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/client/companies-service/companies-swagger -q)'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/client/companies-service/companies-db -q)'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker image rm $(docker images registry.gitlab.com/gusisoft/onelike/client/companies-service/companies -q)'

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} "docker run -d -e 'POSTGRES_USER=postgres' -e 'POSTGRES_PASSWORD=postgres' -p 5434:5432 --name companies-db --network companies-service-network --ip 172.21.0.4 $REGISTRY_REPO/$COMPANIES_DB:$TAG"
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} "docker run -d -e 'API_URL=definitions/swagger.yml' -p 8082:8080 --name companies-swagger --network companies-service-network --ip 172.21.0.3 $REGISTRY_REPO/$SWAGGER:$TAG"
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} "docker run -d -e 'FLASK_ENV=development' -e 'FLASK_APP=manage.py' -e 'APP_SETTINGS=project.config.DevelopmentConfig' -e 'DATABASE_URL=postgres://postgres:postgres@companies-db:5432/companies' -e 'DATABASE_TEST_URL=postgres://postgres:postgres@companies-db:5432/companies_test' -e 'SECRET_KEY=secret_key' -e USERS_SERVICE_URL=$USERS_SERVICE_URL -p 5002:5000 --name companies --network companies-service-network --ip 172.21.0.2 $REGISTRY_REPO/$COMPANIES:$TAG"

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker network connect client-network --ip 172.18.0.7 companies'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker network connect client-network --ip 172.18.0.9 companies-swagger'

ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container exec companies python manage.py recreate-db'
ssh -o StrictHostKeyChecking=no ubuntu@${STAGE_SERVER} 'docker container exec companies python manage.py seed-db'
