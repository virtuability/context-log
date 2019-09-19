""" Module definition
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='context-log',
      description='A simple library to emit contextual information in structured logs (JSON)',
      version='0.1.0',
      author='Morten Jensen',
      author_email='release@virtuability.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/virtuability/context-log',
      packages=find_packages(exclude=["tests"]),
      license='MIT',
      python_requires='>=3.6',
      install_requires=['python_json_logger>=0.1.11', 'PyYAML>=5.1.2'],
      tests_require=['pytest>=5.1.2']
)
