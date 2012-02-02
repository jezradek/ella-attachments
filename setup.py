from setuptools import setup, find_packages

VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'ella_attachments',
    version = __versionstr__,

    packages = find_packages(
        where = '.',
        exclude = ('tests',)
    ),

    include_package_data = True,
)
