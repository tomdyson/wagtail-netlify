from setuptools import setup, find_packages
from wagtailnetlify import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='wagtailnetlify',
    version=__version__,
    description='Deploy Wagtail sites to Netlify',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tomdyson/wagtail-netlify',
    author='Tom Dyson',
    author_email='tom+wagtailnetlify@torchbox.com',
    license='MIT',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 1",
        "Framework :: Wagtail :: 2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords='development',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "wagtail>=1.6",
        "wagtail-bakery>=0.3.0"
    ],
)
