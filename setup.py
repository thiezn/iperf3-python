from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys

from iperf3 import iperf3

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# tox breaks with this in here, need to sort this out
# long_description = read('README.md', 'CHANGES.md')

long_description = 'not so long after all'


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(name='iperf3',
      version=iperf3.__version__,
      url='https://github.com/thiezn/iperf3-python',
      author='Mathijs Mortimer',
      tests_require=['pytest'],
      install_requires=[],
      cmdclass={'test': PyTest},
      description='Wrapper around iperf3 using libiperf API',
      keywords='iperf3 iperf',
      long_description=long_description,
      include_package_data=True,
      platforms='any',
      test_suite='iperf3.test.test_iperf3',
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers, Network Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        ],
      extras_require={'testing': ['iperf3']},
      author_email='mathijs@mortimer.nl',
      license='MIT',
      packages=['iperf3'])
