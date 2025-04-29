from setuptools import setup

__title__ = 'pycot'
__version__ = '3.0.0'
__author__ = 'William Crum'
__license__ = 'Apache 2.0 License'

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="PyCoT",
    version="3.0.1",
    description="Python Cursor On Target Object-Relational Mapper",
    author="William Crum",
    author_email="will@wcrum.dev",
    url=f'https://github.com/ampledata/{__title__}',
    packages=["CoT", "CoT.models", "CoT.xml"],
    install_requires=[
        "pydantic>=1.10.2",
        "xmltodict>=0.13.0",
    ],
    extras_require={
        "mitre": ["PyCoT-MITRE"],
        "ais": ["pyais"]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
