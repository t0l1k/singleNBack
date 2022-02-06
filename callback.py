class Signal:
    'A simple signal - slot mechanism'

    def __init__(self) -> None:
        self.slots = []

    def connect(self, slot):
        'slot is a function'
        assert callable(slot)
        self.slots.append(slot)

    def __call__(self, *args, **kwds):
        for slot in self.slots:
            slot(*args, **kwds)
