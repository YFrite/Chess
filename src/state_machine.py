
class StateMachine(object):
    def __init__(self):
        self.done = False
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.now = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, keys, now):
        self.now = now
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(keys, now)

    def draw(self, surface, interpolate):
        self.state.draw(surface, interpolate)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.now, persist)
        self.state.previous = previous
        print(f"{self.state.previous} -> {self.state_name}")

    def get_event(self, event):
        self.state.get_event(event)


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.now = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}
        print()

    def get_event(self, event):
        pass

    def startup(self, now, persistent):
        self.persist = persistent
        self.start_time = now

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, keys, now):
        raise NotImplemented()
