import unittest
from pubsub import PubSub, Events

class PubSubSubscribeTestCase(unittest.TestCase):
    def setUp(self):
        self.pubsub = PubSub()

    def test_new_event_subscriber(self):
        self.pubsub.clear_all()
        self.pubsub.subscribe(Events.EVENT_NONE, None)
        self.assertEqual(1, len(self.pubsub.subscribers))
        self.assertTrue(Events.EVENT_NONE in self.pubsub.subscribers)
        self.assertTrue(None in self.pubsub.subscribers[Events.EVENT_NONE])
        self.pubsub.subscribe(Events.EVENT_BIND_BUTTON_CLICKED, None)
        self.assertEqual(2, len(self.pubsub.subscribers))
        self.assertTrue(Events.EVENT_NONE in self.pubsub.subscribers)
        self.assertTrue(Events.EVENT_BIND_BUTTON_CLICKED in self.pubsub.subscribers)
        self.assertTrue(None in self.pubsub.subscribers[Events.EVENT_NONE])
        self.assertTrue(None in self.pubsub.subscribers[Events.EVENT_BIND_BUTTON_CLICKED])

    def test_existing_event_subscriber(self):
        self.pubsub.clear_all()
        self.pubsub.subscribe(Events.EVENT_NONE, None)
        self.pubsub.subscribe(Events.EVENT_NONE, None)
        self.assertEqual(1, len(self.pubsub.subscribers))
        self.assertTrue(Events.EVENT_NONE in self.pubsub.subscribers)
        self.assertEqual(2, len(self.pubsub.subscribers[Events.EVENT_NONE]))
        self.assertEqual([None, None], self.pubsub.subscribers[Events.EVENT_NONE])

class PubSubPublishTestCase(unittest.TestCase):
    def setUp(self):
        self.pubsub = PubSub()

    def test_publish_one_subscriber(self):
        self.pubsub.clear_all()
        self.pubsub.subscribe(Events.EVENT_NONE, self.event_handler_publish_one_subscriber)
        self.pubsub.publish(Events.EVENT_NONE, 0)
    
    def event_handler_publish_one_subscriber(self, data):
        self.assertEqual(0, data)

    def test_publish_multi_subscribers(self):
        self.pubsub.clear_all()
        self.pubsub.subscribe(Events.EVENT_NONE, self.event_handler_publish_multi_subscribers_01)
        self.pubsub.subscribe(Events.EVENT_NONE, self.event_handler_publish_multi_subscribers_02)
        self.pubsub.subscribe(Events.EVENT_NONE, self.event_handler_publish_multi_subscribers_03)
        self.pubsub.publish(Events.EVENT_NONE, [1, 2, 3])
    
    def event_handler_publish_multi_subscribers_01(self, data):
        self.assertTrue(1 in data)
    def event_handler_publish_multi_subscribers_02(self, data):
        self.assertTrue(2 in data)
    def event_handler_publish_multi_subscribers_03(self, data):
        self.assertTrue(3 in data)

    def test_publish_multi_events(self):
        self.pubsub.clear_all()
        self.pubsub.subscribe(Events.EVENT_BIND_BUTTON_CLICKED, self.event_handler_bind)
        self.pubsub.subscribe(Events.EVENT_NONE, self.event_handler_none)
        self.pubsub.publish(Events.EVENT_BIND_BUTTON_CLICKED, (1, 2))
        self.pubsub.publish(Events.EVENT_NONE, None)

    def event_handler_bind(self, data):
        self.assertEqual((1, 2), data)
    def event_handler_none(self, data):
        self.assertEqual(None, data)


if __name__ == '__main__':
    unittest.main()
