from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="WebPageLinkMiner",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for extracting all the links from a given domain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/WebPageLinkMiner",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.8.4",
        "aiosignal==1.3.1",
        "beautifulsoup4==4.12.2",
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "async-timeout==4.0.2",
        "lxml==4.9.2",
        "multidict==6.0.4",
        "nest-asyncio==1.5.6",
        "requests==2.31.0",
        "urllib3==2.0.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
