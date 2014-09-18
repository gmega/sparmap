from setuptools import setup

setup(name='parmap',
      version='0.2',
      description='Simple parallel map implementation for Python.',
      author='Giuliano Mega',
      author_email='mega@spaziodati.eu',
      py_modules=['parmap'],
      license="LICENSE",
      install_requires=[
          "multiprocessing >= 2.6.2.1"
      ]
)
