from setuptools import setup, find_packages
import setuptools_scm

with open('README.md', encoding='utf-8') as readme_file:
   README = readme_file.read()

setup(
   name="npdatetime",
   use_scm_version=True,
   packages=find_packages(where=".", include=["npdatetime", "npdatetime.*"]),
   setup_requires=["setuptools_scm"],
   description="A Python package that provides advanced functionality for handling Nepali dates and times, including support for the Bikram Sambat calendar system and Nepal Time (NPT). Ideal for developers working with Nepali date-related applications, offering seamless conversion, manipulation, and formatting of dates and times in the Nepali calendar.",
   long_description=README,
   long_description_content_type="text/markdown",
   url="https://github.com/4mritGiri/npdatetime",
   author="Amrit Giri",
   author_email="amritgiri02595@gmail.com",
   license="MIT",
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
