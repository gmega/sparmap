from distutils.core import setup

setup(
    name='sparmap',
    version='1.0.3',
    description='Simple parallel map implementation for Python.',
    author='Giuliano Mega',
    author_email='mega@spaziodati.eu',
    py_modules=['sparmap'],
    license='LICENSE',
    install_requires=[
        'multiprocessing >= 2.6.2.1'
    ],
    tests_require=['nose'],
    url=['https://github.com/gmega/parmap'],
)
