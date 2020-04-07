from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="transcov",
    version="1.0.1",
    author="Per Høgfeldt",
    description="A software for mapping coverage around transcription start sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hogfeldt/transcov",
    packages=find_packages("src"),
    package_dir={"": "src"},
    # test_suite="test",
    install_requires=[
        "pysam>=0.15.4",
        "numpy>=1.18.1",
        "attrs>=19.3.0",
        "click>=7.1.1",
    ],
    entry_points={"console_scripts": ["transcov = transcov.cli:cli"],},
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
