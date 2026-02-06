"""
Django NPDateTime - Nepali Date Field and Picker for Django
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-npdatetime',
    version='0.1.0',
    description='Nepali Date Field and Date Picker Widget for Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Amrit Giri',
    author_email='amritgiri.dev@gmail.com',
    url='https://github.com/4mritGiri/npdatetime-rust',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'npdatetime>=0.1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='django nepali bikram sambat date picker calendar',
    project_urls={
        'Bug Reports': 'https://github.com/4mritGiri/npdatetime-rust/issues',
        'Source': 'https://github.com/4mritGiri/npdatetime-rust',
        'Documentation': 'https://github.com/4mritGiri/npdatetime-rust/tree/main/bindings/django',
    },
)
