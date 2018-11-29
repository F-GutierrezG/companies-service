#!/bin/bash

type=$1

watchTests() {
  docker container exec companies ptw -cn --runner "python manage.py test"
}

test() {
  docker container exec companies python manage.py test
}

if [[ "${type}" == "watch" ]]; then
  echo "\n"
  echo "Testing!"
  watchTests
else
  echo "\n"
  echo "Testing!"
  test
fi
