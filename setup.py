from setuptools import setup, find_packages

setup(
    name="simplealpaca",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "alpaca-py",
    ],
    author="Conor Van Bibber",
    author_email="cvanbibber@berkeley.edu",
    description="A simple but comprehensive Alpaca trading API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simplealpaca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
