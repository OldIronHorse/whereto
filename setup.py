from setuptools import setup

setup(name='whereto',
      version='0.1',
      description='How far can I get in N hours?',
      url='http://github.com/oldironhorse/whereto',
      license='GPL 3.0',
      packages=['whereto'],
      install_requires=['flask'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
