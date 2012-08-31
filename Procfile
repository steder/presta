queue: rabbitmq-server
mongo: mongod run --config /usr/local/etc/mongod.conf
#periodic: celery beat --app presta --loglevel=INFO --broker=amqp://rabbit@localhost//
worker: celery worker --app presta --loglevel=INFO --broker=amqp://rabbit@localhost//
web: ./bin/twistr -n web --user --port=8000
