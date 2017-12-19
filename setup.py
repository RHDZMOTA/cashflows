from setuptools import setup

setup(name='cashflows',
      version='0.1',
      description='Cashflow analysis utils',
      url='http://github.com/rhdzmota/cashflows',
      author='rhdzmota',
      author_email='rohdzmota@gmail.com',
      license='MIT',
      packages=['cashflows'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
