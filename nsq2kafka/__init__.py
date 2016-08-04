from kafka import KafkaProducer
import nsq
import json
import signal
import logging
import tornado.ioloop


class NSQ2Kafka(object):
    """ Reads from an NSQ topic and publishes to
    a single Kafka stream

    Arguments should be passed in the form of <nsq|kafka>_kwarg

    Where kwarg is the kwarg for either nsq.Reader or kafka.KafkaProducer

    Example:
        NSQ2Kafka(nsq_topic='nsq_test', nsq_nsqd_tcp_addresses='localhost', kafka_topic='kafka_test')
    """

    def __init__(self, **kwargs):
        nsq_args = {k[4:]: v for (k, v) in kwargs.items() if k[:3] == 'nsq' and v is not None}
        kafka_args = {k[6:]: v for (k, v) in kwargs.items() if k[:4] == 'kafka' and v is not None}

        self._nsq_topic = nsq_args.pop('topic', None)
        if self._nsq_topic is None:
            raise TypeError('nsq_topic is required')

        self._nsq_channel = nsq_args.pop('channel', 'nsq2kafka#ephemeral')
        self._message_key = kafka_args.pop('message_key', None)
        self._kafka_topic = kafka_args.pop('topic', self._nsq_topic)

        self._nsq = nsq.Reader(self._nsq_topic, self._nsq_channel, message_handler=self._on_message, **nsq_args)
        self._kafka = KafkaProducer(**kafka_args)

    @staticmethod
    def _on_publish_complete(value, nsq_message):
        logging.debug('Finishing nsq_message %s', value)
        nsq_message.finish()

    @staticmethod
    def _on_publish_error(exc, nsq_message):
        logging.error('Could error publishing message %s', nsq_message)
        logging.exception(exc.message)
        nsq_message.requeue()

    def _on_message(self, nsq_message):
        nsq_message.enable_async()
        key = None
        if self._message_key is not None:
            message = json.loads(nsq_message.body)
            key = message.get(self._message_key)

        future = self._kafka.send(self._kafka_topic, key=key, value=nsq_message.body)
        future.add_callback(self._on_publish_complete, nsq_message=nsq_message)
        future.add_errback(self._on_publish_error, nsq_message=nsq_message)

    def _term_handler(self, sig_num, frame):
        logging.info('TERM Signal handler called with signal %r', sig_num)
        self.stop()

    def start(self):
        """
        Starts reading from NSQ and publishing to Kafka
        """
        logging.info('Starting NSQ2Kafka "%s/%s" => Kafka "%s"', self._nsq_topic, self._nsq_channel, self._kafka_topic)
        signal.signal(signal.SIGTERM, self._term_handler)
        signal.signal(signal.SIGINT, self._term_handler)
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        """
        Stops reading from NSQ, flushes Kafka and ACKs in-flight NSQ messages
        :return:
        """
        logging.info('Flushing Kafka producer')
        self._kafka.flush()
        logging.info('Stopping NSQ')
        self._nsq.close()
        tornado.ioloop.IOLoop.instance().stop()
