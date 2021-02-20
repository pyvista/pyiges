"""Setup for pyiges"""
from setuptools import setup
import os
from io import open as io_open

# Get version
__version__ = None
filepath = os.path.dirname(__file__)
version_file = os.path.join(filepath, 'pyiges', '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())

readme_file = os.path.join(filepath, 'README.rst')

setup(
    name='pyiges',
    packages=['pyiges', 'pyiges.examples'],
    version=__version__,
    author='PyVista Developers',
    author_email='info@pyvista.org',
    long_description=io_open(readme_file, encoding="utf-8").read(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Pythonic IGES reader',
    url='https://github.com/pyvista/pyiges',
    install_requires=['tqdm', 'geomdl', 'pyvista>=0.28.0'],
    package_data={'pyiges.examples': ['impeller.igs', 'sample.igs']}
)
