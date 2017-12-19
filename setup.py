# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = '0.1'

install_requires = [
    'setuptools',
    'cromlech.session',
    'cromlech.marshallers',
    'itsdangerous',
    'biscuits',
    'redis',
]

tests_require = [
    'WebTest',
    'pytest',
    'pytest-redis >= 1.3.2',
]

setup(
    name='cromlech.sessions.redis',
    version=version,
    description="Session handling for wsgi applications using redis",
    long_description=(
        open("README.md").read() + "\n" +
        open(os.path.join("docs", "HISTORY.txt")).read()),
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='Cromlech Session',
    author='The Dolmen team',
    author_email='dolmen@list.dolmen-project.org',
    url='http://gitweb.dolmen-project.org/',
    license='ZPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['cromlech', 'cromlech.sessions'],
    include_package_data=True,
    zip_safe=False,
    tests_require=tests_require,
    install_requires=install_requires,
    extras_require={'test': tests_require},
)
