from enum import IntEnum, auto

class Events(IntEnum):
    EVENT_BIND_BUTTON_CLICKED = 0
    EVENT_NONE = auto()

class PubSub():
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, event_handler):
        if event not in Events:
            return

        if event not in self.subscribers:
            self.subscribers[event] = []

        self.subscribers[event].append(event_handler)

    def publish(self, event, data):
        if event in self.subscribers:
            handlers = self.subscribers[event]

            for handler in handlers:
                if handler is not None:
                    handler(data)

    def clear_all(self):
        self.subscribers = {}
