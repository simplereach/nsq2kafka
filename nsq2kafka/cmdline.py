from nsq2kafka import NSQ2Kafka
import tornado.options
import tornado.log


def main():
    tornado.options.define('nsq_topic',
                           type=str,
                           group='NSQ',
                           help='specifies the desired NSQ topic')
    tornado.options.define('nsq_channel',
                           type=str,
                           group='NSQ',
                           default='nsq2kafka#ephemeral',
                           help='specifies the desired NSQ channel')
    tornado.options.define('nsq_nsqd_tcp_addresses',
                           type=str,
                           multiple=True,
                           group='NSQ',
                           help='a sequence of string addresses of the nsqd instances this reader should connect to')
    tornado.options.define('nsq_lookupd_http_addresses',
                           type=str,
                           multiple=True,
                           group='NSQ',
                           help='a sequence of string addresses of the nsqlookupd instances this reader should query '
                                'for producers of the specified topic')
    tornado.options.define('nsq_max_in_flight',
                           type=int,
                           default=500,
                           group='NSQ',
                           help='the maximum number of messages this reader will pipeline for processing. this value '
                                'will be divided evenly amongst the configured/discovered nsqd producers')
    tornado.options.define('kafka_bootstrap_servers',
                           type=str,
                           group='Kafka',
                           default='localhost:9092',
                           multiple=True,
                           help='host[:port] string (or list of host[:port] strings) that the producer should contact '
                                'to bootstrap initial cluster metadata')
    tornado.options.define('kafka_topic',
                           type=str,
                           group='Kafka',
                           help='The Kafka Topic to publish the messages')
    tornado.options.define('kafka_message_key',
                           type=str,
                           group='Kafka',
                           help='When the message is in JSON format, use a key from the message to determine the kafka '
                                'partition')

    tornado.options.parse_command_line()

    nsq2kafka = NSQ2Kafka(**tornado.options.options.as_dict())
    nsq2kafka.start()

if __name__ == '__main__':
    exit(main())
