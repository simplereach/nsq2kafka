nsq2kafka
=========

Reads from NSQ, Publishes to Kafka

Installation
~~~~~~~~~~~~

::

    pip install nsq2kafka

Examples
~~~~~~~~

Basic example

::

    nsq2kafka --nsq-topic=test --nsq-nsqd-tcp-addresses=localhost:4150

Realistic example

::

    nsq2kafka --nsq-topic=json_clicks \
              --nsq-lookupd-http-addresses=lookupd1.example.com:4161,lookupd2.example.com:4161 \
              --nsq-max-in-flight=5000 \
              --nsq-channel=nsq2Kafka \
              --kafka-bootstrap-servers=kafka1.example.com:9092,kafka2.exampkel.com:9092 \
              --kafka-topic=click_stream_json \
              --kafka-message-key=user_id
