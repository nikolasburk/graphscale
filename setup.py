from setuptools import find_packages, setup

setup(
    name='graphscale',
    version='0.0.1',
    description='GraphQL API Server Framework for Python',
    long_description=open('README.rst').read(),
    url='https://github.com/schrockn/graphscale',
    author='Nicholas Schrock',
    author_email='schrockn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Environment :: MacOS X',
    ],
    keywords='api graphql protocol rest relay graphscale',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'aiodataloader>=0.1.2',
        'aoiklivereload',
        # must install the following from local copies
        #'graphql-core',
        #'graphql-server-core',
        #'sanic-graphql',
        'iso8601>=0.1.11',
        'promise>=2.0.2',
        'py>=1.4.34',
        'PyMySQL>=0.7.11',
        'redis>=2.10.5',
        'six>=1.10.0',
        'typing>=3.6.1',
        # just putting all dev/test deps in here for now
        'pytest>=3.1.3',
        'pytest-asyncio>=0.6.0',
        'mypy>=0.511',
        'mypy-extensions>=0.2.0',
        'snapshottest>=0.5.0',
    ],
)
