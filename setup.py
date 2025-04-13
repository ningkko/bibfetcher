# setup.py
from setuptools import setup, find_packages

setup(
    name="bibfetcher",
    version="0.1",
    description="Fetch BibTeX from article titles using CrossRef",
    author="Ning Hua",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'bibfetcher = bibfetcher.main:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
