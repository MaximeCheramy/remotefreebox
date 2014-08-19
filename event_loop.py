import time
import select


class event_source(object):
    def __init__(self, callback, args=None):
        self.when = None
        self.callback = callback
        self.args = args

    def call(self):
        if self.args is not None:
            self.callback(*self.args)
        else:
            self.callback()


class event_loop(object):
    def __init__(self):
        self.events = []
        self.objects = {}

    def add(self, event):
        if event not in self.events:
            self.events.append(event)

    def remove(self, event):
        self.events[:] = [x for x in self.events if x is not event]

    def add_object(self, obj, callback, args=None):
        self.objects[obj] = (callback, args)

    def loop(self):
        while True:
            objs, _, _ = select.select(self.objects.keys(), [], [], 0)
            for obj in objs:
                callback, args = self.objects[obj]
                if args is None:
                    callback()
                else:
                    callback(*args)

            toremove = []
            for evt in self.events:
                if evt.when <= time.time() * 1000:
                    evt.call()
                    toremove.append(evt)
            if toremove:
                self.events[:] = [evt for evt in self.events
                                  if evt not in toremove]
            else:
                time.sleep(.001)
