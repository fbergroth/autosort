from collections import namedtuple


class Name(namedtuple('Name', 'names asname')):
    CAMEL, SNAKE, CONST = range(3)

    @classmethod
    def from_str(cls, name, asname):
        return cls(tuple(name.split('.')), asname)

    @property
    def top(self):
        return self.names[0]

    @classmethod
    def kind(cls, name):
        part = name.lstrip('_')
        if part.isupper():
            kind = cls.CONST
        elif part and part[0].isupper():
            kind = cls.CAMEL
        else:
            kind = cls.SNAKE
        return len(name) - len(part), kind

    @property
    def key(self):
        return [(self.kind(name), name) for name in self.names]

    def __lt__(self, other):
        return self.key < other.key

    def __str__(self):
        name = '.'.join(self.names)
        return '{0} as {1}'.format(name, self.asname) if self.asname else name


class Module(namedtuple('Module', 'name level')):
    DUNDER, STDLIB, THIRDPARTY, LOCAL, RELATIVE = range(5)

    def kind(self, config):
        top = self.name.top
        if self.level > 0:
            return self.RELATIVE
        if top in config['local_modules']:
            return self.LOCAL
        if top in config['dunders']:
            return self.DUNDER
        if top in config['stdlib']:
            return self.STDLIB
        return self.THIRDPARTY

    def __str__(self):
        return '{0}{1}'.format('.' * self.level, self.name)

    def __lt__(self, other):
        return (-self.level, self.name) < (-other.level, other.name)


class Import(namedtuple('Import', 'kind module names noqa start end')):

    def merge(self, other):
        names = sorted(set(self.names + other.names))
        noqa = self.noqa or other.noqa
        return Import(self.kind, self.module, names, noqa, -1, -1)


Block = namedtuple('Block', 'imports indent start')
