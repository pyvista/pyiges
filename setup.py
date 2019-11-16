"""Setup for pyiges"""
from setuptools import setup
import os
from io import open as io_open

package_name = 'pyiges'

# Get version
__version__ = None
filepath = os.path.dirname(__file__)
version_file = os.path.join(filepath, package_name, '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())

readme_file = os.path.join(filepath, 'README.rst')

setup(
    name=package_name,
    packages = [package_name],
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Pythonic IGES reader',
    url='https://github.com/pyvista/pyiges',
    install_requires=['tqdm', 'geomdl', 'pyvista>=0.22.0'],
    package_data={'pyiges.examples': ['impeller.igs']}
)
