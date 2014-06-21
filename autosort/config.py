import os

py34packages = set([
    '__future__', '__main__', '_dummy_thread', '_thread', 'abc', 'aifc',
    'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit',
    'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins',
    'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code',
    'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent',
    'configparser', 'contextlib', 'copy', 'copyreg', 'cProfile', 'crypt',
    'csv', 'ctypes', 'curses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis',
    'distutils', 'doctest', 'dummy_threading', 'email', 'encodings',
    'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp',
    'fileinput', 'fnmatch', 'formatter', 'fpectl', 'fractions', 'ftplib',
    'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
    'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp',
    'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword',
    'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'macpath', 'mailbox',
    'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder',
    'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib',
    'numbers', 'operator', 'optparse', 'os', 'ossaudiodev', 'parser',
    'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform',
    'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd',
    'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're',
    'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched',
    'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site',
    'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3',
    'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct',
    'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog',
    'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test',
    'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize',
    'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types',
    'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings',
    'wave', 'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib',
    'xml', 'xmlrpc', 'zipfile', 'zipimport', 'zlib',
])

default = dict(local_modules=[], dunders=['__future__'],
               stdlib=py34packages, limit=80)


def lookup_package(path):
    path = os.path.dirname(os.path.abspath(path))
    name = None
    while os.path.exists(os.path.join(path, '__init__.py')):
        path, name = os.path.split(path)

    return name


# TODO
def get_config(path):
    config = default
    name = lookup_package(path)
    if name:
        config['local_modules'].append(name)
    return config
