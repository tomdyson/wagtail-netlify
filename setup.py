from setuptools import setup, find_packages
from wagtailnetlify import __version__

setup(
    name='wagtailnetlify',
    version=__version__,
    description='Deploy Wagtail sites to Netlify',
    long_description='See https://github.com/tomdyson/wagtail-netlify for details',
    url='https://github.com/tomdyson/wagtail-netlify',
    author='Tom Dyson',
    author_email='tom+wagtailnetlify@torchbox.com',
    license='MIT',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 1",
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
        "wagtail-bakery>=0.1.0"
    ],
)
