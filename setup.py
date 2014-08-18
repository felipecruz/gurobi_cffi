from setuptools import setup

setup(name='gurobi_cffi',
      version='0.1',
      description='Gurobi cffi bindings',
      author='Felipe Cruz',
      author_email='felipecruz@loogica.net',
      url='https://github.com/felipecruz/gurobi_cffi',
      install_requires=['cffi>=0.6'],
      packages=['gurobi_cffi'])
