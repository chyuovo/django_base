class EventsException(Exception):
    pass


class Events:
    """
    将核心封装为事件订阅和事件触发，并感觉
    就像语言的“自然”部分。
    类Events的存在主要有三个原因:
    —事件(槽位)是自动添加的，不需要添加
    分别声明/创建它们。这对于原型制作非常有用。(注意
    ' __events__ '是可选的，应该主要帮助检测
    事件名称拼写错误。)
    -提供(和封装)某种程度的自省。
    -“钢的名字”，并在此删除不必要的冗余呼叫
    如:
    xxx。OnChange = event('OnChange')
    """

    def __init__(self, events=None):

        if events is not None:

            try:
                iter(events)
            except:
                raise AttributeError("type object %s is not iterable" %
                                     (type(events)))
            else:
                self.__events__ = events

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))

        if hasattr(self, '__events__'):
            if name not in self.__events__:
                raise EventsException("Event '%s' is not declared" % name)

        elif hasattr(self.__class__, '__events__'):
            if name not in self.__class__.__events__:
                raise EventsException("Event '%s' is not declared" % name)

        self.__dict__[name] = ev = _EventSlot(name)
        return ev

    def __repr__(self):
        return '<%s.%s object at %s>' % (self.__class__.__module__,
                                         self.__class__.__name__,
                                         hex(id(self)))

    __str__ = __repr__

    def __len__(self):
        return len(self.__dict__.items())

    def __iter__(self):
        def gen(dictitems=self.__dict__.items()):
            for attr, val in dictitems:
                if isinstance(val, _EventSlot):
                    yield val

        return gen()


class _EventSlot:
    def __init__(self, name):
        self.targets = []
        self.__name__ = name

    def __repr__(self):
        return "event '%s'" % self.__name__

    def __call__(self, *a, **kw):
        for f in tuple(self.targets):
            f(*a, **kw)

    def __iadd__(self, f):
        self.targets.append(f)
        return self

    def __isub__(self, f):
        while f in self.targets:
            self.targets.remove(f)
        return self

    def __len__(self):
        return len(self.targets)

    def __iter__(self):
        def gen():
            for target in self.targets:
                yield target

        return gen()

    def __getitem__(self, key):
        return self.targets[key]
