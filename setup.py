#!/usr/bin/env python3
"""
Setup.py for Violet DJ Mixer

Allows installation via:
    python3 setup.py install
    pip install .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="violet-dj-mixer",
    version="2.0.0",
    author="Violet DJ Community",
    author_email="support@violet-dj.github.io",
    description="Professional Digital DJ Mixing Board for Ubuntu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/violet-dj/violet-dj-mixer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "violet-dj=main:main",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/violet-dj/violet-dj-mixer/issues",
        "Documentation": "https://violet-dj.github.io",
        "Source Code": "https://github.com/violet-dj/violet-dj-mixer",
    },
)
