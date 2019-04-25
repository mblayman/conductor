from setuptools import find_packages, setup

setup(
    name="conductor",
    version="1.0",
    packages=find_packages(exclude=["settings"]),
    include_package_data=True,
)
