from setuptools import setup, find_packages

setup(
    name='pxlr',  
    version='0.1',
    packages=find_packages(),  
    install_requires=[
        'psutil',  
        'rich',
    ],
    include_package_data=True,  
)
