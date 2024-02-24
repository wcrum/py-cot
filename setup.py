from setuptools import setup

setup(
    name="PyCoT",
    version="0.3",
    description="Python Cursor On Target Object-Relational Mapper",
    author="William Crum",
    author_email="will@wcrum.dev",
    packages=["CoT", "CoT.models", "CoT.xml", "CoT.models"],
    install_requires=[
        "pydantic>=1.10.2",
        "xmltodict>=0.13.0",
    ],
)
