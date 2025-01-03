from setuptools import setup, find_packages

from npdatetime import __version__, __author__

with open('README.md', encoding='utf-8') as readme_file:
   README = readme_file.read()

setup(
   name="npdatetime",
   version=__version__,
   description="Datetime module that operates on top of Bikram Sambat Date & Nepal Time.",
   long_description=README,
   long_description_content_type="text/markdown",
   url="https://github.com/4mritGiri/npdatetime",
   author=__author__,
   author_email="amritgiri02595@gmail.com",
   license="MIT",
   packages=find_packages(exclude=("tests", "docs")),
   keywords=['nepali', 'bs', 'b.s', 'date', 'datetime', 'time', 'timezone', 'nepal', 'bikram', 'sambat', 'samvat',
            'nepali-date', 'nepali-datetime', 'nepal-time', 'npt', 'nepal-timezone', 'npdatetime', 'npdt'],
   include_package_data=True,
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires='>=3.5',
)