from distutils.core import setup

VERSION = '1.1.0'

setup(
    name='sparmap',
    version=VERSION,
    description='A Simple PARallel MAP implementation for Python.',
    author='Giuliano Mega',
    author_email='mega@spaziodati.eu',
    py_modules=['sparmap'],
    license='Apache License 2.0',
    install_requires=[
        'multiprocessing >= 2.6.2.1'
    ],
    tests_require=['nose'],
    url=['https://github.com/gmega/sparmap'],
    download_url='https://github.com/gmega/sparmap/archive/%s.tar.gz' % VERSION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
    ]
)
