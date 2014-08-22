from setuptools import setup

setup(name='parmap',
      version='0.1',
      description='Simple parallel map implementation for Python.',
      author='Giuliano Mega',
      author_email='mega@spaziodati.eu',
      packages=['parmap'],
      license="LICENSE",
      install_requires=[
          "multiprocessing >= 2.6.2.1"
      ]
)