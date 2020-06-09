from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bookkeeper",
    version="0.1.0",
    author="Adrien Cosson",
    author_email="adrien@cosson.io",
    description="The Bookkeeper code for the Sentinel experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdrienCos/bookeeper",
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy'
    ],
    python_requires=">=3.5"
)
