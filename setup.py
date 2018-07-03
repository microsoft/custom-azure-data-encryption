from setuptools import setup, find_packages

requirements = [
    "azure.common",
    "azure.keyvault",
    "cryptography"
]

setup(
    name="azure-custom-data-encryption",
    version="0.0.1",
    description="",
    long_description="",
    url="",
    packages=find_packages(include=["app"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ]
)
