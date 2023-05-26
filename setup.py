from setuptools import setup, find_packages

setup(
    name="webpagelinkminer",
    version="0.1",
    packages=find_packages(),
    description="A tool for extracting all links from the same domain using a base URL",
    author="Ojas Kapre",
    author_email="ojasskapre@gmail.com",
    url="https://github.com/ojasskapre/webpagelinkminer",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "aiohttp",
    ],
    python_requires='>=3.8',
)
