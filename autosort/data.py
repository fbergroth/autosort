from collections import namedtuple


class Name(namedtuple('Name', 'name asname')):
    CAMEL, SNAKE, CONST = range(3)

    @property
    def kind(self):
        name = self.name.split('.')[-1]
        if name.isupper():
            return self.CONST
        if name[0].isupper():
            return self.CAMEL
        return self.SNAKE

    def key(self):
        return self.kind, str(self)

    def __str__(self):
        if self.asname:
            return '{0} as {1}'.format(self.name, self.asname)
        return self.name


class Module(namedtuple('Module', 'name level')):
    DUNDER, STDLIB, THIRDPARTY, LOCAL, RELATIVE = range(5)

    def kind(self, config):
        name = self.name.name.split('.')[0]

        if self.level > 0:
            return self.RELATIVE
        if name in config['local_modules']:
            return self.LOCAL
        if name in config['dunders']:
            return self.DUNDER
        if name in config['stdlib']:
            return self.STDLIB
        return self.THIRDPARTY

    def __str__(self):
        return '{0}{1}'.format('.' * self.level, self.name)


class Import(namedtuple('Import', 'kind module names noqa start end')):

    def merge(self, other):
        names = sorted(set(self.names + other.names), key=Name.key)
        noqa = self.noqa or other.noqa
        return Import(self.kind, self.module, names, noqa, -1, -1)


Block = namedtuple('Block', 'imports indent start')
