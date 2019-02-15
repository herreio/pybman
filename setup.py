import os
import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pybman",
    version="2019.02.15",
    author="Donatus Herre",
    author_email="pypi@herre.io",
    maintainer="Donatus Herre",
    maintainer_email="pypi@herre.io",
    license="GPLv3",
    description="Python package (under development) for interacting with MPG.PuRe",
    long_description=README,
    url="https://github.com/herreio/pybman/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
)
