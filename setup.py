from setuptools import setup, find_packages

# Package meta-data
NAME = "transcov"
DESCRIPTION = ""

setup(
    name = "transcov",
    description = "A software for mapping coverage around transcription start sites",
    packages=find_packages("src"),
    package_dir={"": "src"},
    #test_suite="test",
    install_requires=['pysam'],
    entry_points={
         'console_scripts': ['transcov = transcov.cli:start'],
    },
    include_package_data=True,
)

