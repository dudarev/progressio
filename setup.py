#!/usr/bin/env python

from progressio.progressio import __version__

# The current version of the system.  Format is #.#.#[-DEV].
version = __version__

import distutils.sysconfig

# Require Python 2.7 or higher, but not 3.x
py_ver = distutils.sysconfig.get_python_version()
if (py_ver < '2.7') or (py_ver >= '3.0'):
    raise ValueError('wsapi requires Python version 2.x where x >= 7 (you have %s)' % (py_ver,))

import os
import datetime

from distutils.core import setup, Command


# a command that automaticaly updates version number
# taken from pyxb sourcecode
class update_readme(Command):
    # Brief (40-50 characters) description of the command
    description = "Substitute @VERSION@ in relevant files"

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = []
    boolean_options = []

    # Files in the distribution that need to be rewritten when the
    # version number changes
    files = ('README.md', )

    # The substitutions (key braced by @ signs)
    substitutions = {
        'VERSION': version,
        'THIS_YEAR': datetime.date.today().strftime('%Y'),
        'SHORTVERSION': '.'.join(version.split('.')[:2])}

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for f in self.files:
            text = file('%s.in' % (f,)).read()
            for (k, v) in self.substitutions.items():
                text = text.replace('@%s@' % (k,), v)
            file(f, 'w').write(text)

setup_path = os.path.dirname(__file__)
possible_bundles = []

setup(
    name='progressio',
    description='A file-based project management and bug-tracking tool.',
    author='Artem Dudarev',
    author_email='dudarev@gmail.com',
    url='https://github.com/dudarev/progressio',
    version=version,
    license='New BSD License',
    long_description='''
''',
    provides=['progressio'],
    cmdclass={'update_readme': update_readme},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities'],
    scripts=['progressio/p'],
    packages=['progressio'],
    requires=[],
)
