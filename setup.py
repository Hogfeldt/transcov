from setuptools import setup, find_packages

setup(
    name = "transcov",
    description = "A software for mapping coverage around transcription start sites",
    packages=find_packages("src"),
    package_dir={"": "src"},
    #test_suite="test",
    install_requires=['pysam>=0.15.4', 'numpy>=1.18.1', 'attrs>=19.3.0', 'click>=7.1.1'],
    entry_points={
        'console_scripts': ['transcov = transcov.cli:cli'],
    },
    include_package_data=True,
)

