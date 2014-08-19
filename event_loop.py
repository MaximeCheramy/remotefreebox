import bisect
import time
import select


class event_loop(object):
    def __init__(self):
        self.events = []
        self.objects = {}

    def add(self, when, callback, args=None):
        bisect.insort_right(self.events, (when, callback, args))

    def remove(self, callback):
        self.events[:] = [x for x in self.events if x[1] is not callback]

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
            if self.events and self.events[-1][0] <= time.time() * 1000:
                evt = self.events.pop()
                if evt[2] is None:
                    evt[1]()
                else:
                    evt[1](*evt[2])
            else:
                time.sleep(.001)
