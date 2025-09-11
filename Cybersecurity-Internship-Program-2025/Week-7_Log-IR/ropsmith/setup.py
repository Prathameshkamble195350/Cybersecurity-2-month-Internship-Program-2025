from setuptools import setup, find_packages

setup(
    name="ropsmith",
    version="1.0.0",
    description="Return-Oriented Programming (ROP) Chain Exploration Tool",
    author="ACCSI Offensive Security Lab",
    packages=find_packages(),
    install_requires=[
        "capstone",
        "networkx",
        "flask",
        "graphviz"
    ],
    entry_points={
        "console_scripts": [
            "ropsmith=ropsmith.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
