from distutils.core import setup

setup(
    name='sparmap',
    version='1.1.0',
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
    download_url='https://github.com/gmega/sparmap/archive/1.0.4.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
    ]
)
