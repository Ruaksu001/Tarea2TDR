FROM rabbitmq:3

RUN rabbitmq-plugins enable --offline rabbitmq_management

RUN echo "loopback_users = none" > /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672

