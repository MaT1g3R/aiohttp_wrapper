from setuptools import setup

requirements = [
    'aiohttp>=2.2.5',
    'xmltodict>=0.11.0'
]

packages = ['aiohttp_wrapper']
package_data = {'': ['LICENSE']}

with open('README.md') as f:
    readme = f.read()

__title__ = 'aiohttp_wrapper'
__description__ = ' Abstraction of HTTP requests using aiohttp'
__url__ = 'https://github.com/MaT1g3R/aiohttp_wrapper'
__version__ = '1.0.0'
__author__ = 'MaT1g3R'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 MaT1g3R'

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=readme,
    author=__author__,
    license=__license__,
    include_package_data=True,
    package_data=package_data,
    install_requires=requirements,
    packages=packages,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

    )
)
