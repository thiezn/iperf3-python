from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

from iperf3 import iperf3

here = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    return open("README.rst").read()


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
      long_description=get_long_description(),
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
