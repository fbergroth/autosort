import re
import sys
from setuptools import setup

with open('autosort/__init__.py') as f:
    version = re.search(r'''^__version__\s+=\s+['"](.+)['"]''',
                        f.read(), re.M).group(1)

INSTALL_REQUIRES = ['argparse'] if sys.version_info < (2, 7) else []

setup(name='autosort',
      author='Fredrik Bergroth',
      author_email='fbergroth@gmail.com',
      version=version,
      url='https://github.com/fbergroth/autosort',
      license='MIT',
      packages=['autosort'],
      install_requires=INSTALL_REQUIRES,
      entry_points={'console_scripts': ['autosort = autosort:main']},
      description='Automatically sort import statements.')
