import json
import argparse
from sseclient import SSEClient as EventSource
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from urllib.parse import urlparse

lang_codes = json.loads(open("language-and-locale-codes.json").read())


class Event:
    def __init__(self, event_data):
        self.event_id = event_data['id']
        self.timestamp = event_data['meta']['dt']
        self.username = event_data['user']
        self.user_type = "bot" if not event_data['bot'] else "human"
        self.language = self.get_language(urlparse(event_data["meta"]["uri"]).netloc)
        self.title = event_data['title']

        # Parsing WikiMedia's language codes (JSON format)

    @staticmethod
    def get_language(url: str) -> str:
        for lang in lang_codes:
            if lang["code"] in url:
                return lang["desc"]
        return "English"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def create_kafka_producer(bootstrap_server):
    try:
        kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_server,
                                       value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    except NoBrokersAvailable:
        print('No broker found at {}'.format(bootstrap_server))
        raise

    if kafka_producer.bootstrap_connected():
        print('Kafka producer connected!')
        return kafka_producer
    else:
        print('Failed to establish connection!')
        exit(1)


def construct_event(event_data):
    # user_types = {True: 'bot', False: 'human'}
    # # use dictionary to change assign namespace value and catch any unknown namespaces (like ns 104)
    # try:
    #     event_data['namespace'] = namespace_dict[event_data['namespace']]
    # except KeyError:
    #     event_data['namespace'] = 'unknown'
    #
    # # assign user type value to either bot or human
    # user_type = user_types[event_data['bot']]
    #
    # # define the structure of the json event that will be published to kafka topic
    # event = {"id": event_data['id'],
    #          "title": event_data['title'],
    #          "timestamp": event_data['meta']['dt'],  # event_data['timestamp'],
    #          "username": event_data['user'],
    #          "user_type": user_type,
    #          "lang":
    #          "old_length": event_data['length']['old'],
    #          "new_length": event_data['length']['new']}
    #
    # return event
    pass


def init_namespaces():
    """
    Creates a dictionary for the various known namespaces.
    :return: dict with category name as key and value as value
    """
    namespace = {-2: 'Media',
                 -1: 'Special',
                 0: 'main namespace',
                 1: 'Talk',
                 2: 'User', 3: 'User Talk',
                 4: 'Wikipedia', 5: 'Wikipedia Talk',
                 6: 'File', 7: 'File Talk',
                 8: 'MediaWiki', 9: 'MediaWiki Talk',
                 10: 'Template', 11: 'Template Talk',
                 12: 'Help', 13: 'Help Talk',
                 14: 'Category', 15: 'Category Talk',
                 100: 'Portal', 101: 'Portal Talk',
                 108: 'Book', 109: 'Book Talk',
                 118: 'Draft', 119: 'Draft Talk',
                 446: 'Education Program', 447: 'Education Program Talk',
                 710: 'TimedText', 711: 'TimedText Talk',
                 828: 'Module', 829: 'Module Talk',
                 2300: 'Gadget', 2301: 'Gadget Talk',
                 2302: 'Gadget definition', 2303: 'Gadget definition Talk'}

    return namespace


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='EventStreams Kafka producer')

    parser.add_argument('--bootstrap-server', default='localhost:9092', help='Kafka bootstrap broker(s) (host[:port])',
                        type=str)
    parser.add_argument('--topic-name', default='wikipedia-events', help='Destination topic name', type=str)
    parser.add_argument('--events-to-produce', help='Kill producer after N events have been produced', type=int,
                        default=1000)

    return parser.parse_args()


def process_events(topic_name: str, producer):
    """
    Processes events from EventsSource of Wikipedia.
    :return:
    """
    urls = ['https://stream.wikimedia.org/v2/stream/recentchange',
            'https://stream.wikimedia.org/v2/stream/created']

    filtered_events = ['edit', 'create']
    messages_count = 0

    for url in urls:
        for event in EventSource(url):
            if event.event == 'message':
                try:
                    event_data = json.loads(event.data)
                except ValueError:
                    pass
                else:
                    if event_data['type'] in filtered_events:
                        event_to_send = Event(event_data)
                        producer.send(topic_name, value=event_to_send.to_json())

                        messages_count += 1

            if messages_count >= args.events_to_produce:
                print('Producer will be killed as {} events were produced'.format(args.events_to_produce))
                exit(0)


if __name__ == "__main__":
    # parse command line arguments
    args = parse_command_line_arguments()

    # init dictionary of namespaces
    namespace_dict = init_namespaces()

    # init producer
    kafka_prod = create_kafka_producer(args.bootstrap_server)
    process_events(args.topic_name, kafka_prod)

    print('*** Messages are being published to Kafka topic ***')
