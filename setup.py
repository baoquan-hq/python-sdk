from setuptools import setup, find_packages

setup(
    name='eagle-python-sdk',
    version='1.0.0',
    packages=find_packages(),
    url='https://baoquan.com',
    license='gpl-3.0',
    author='sbwdlihao',
    author_email='sbwdlihao@gmail.com',
    keywords='baoquan eagle sdk',
    description='sdk for members to use the service of baoquan.com',
    long_description=open('README.md').read(),
    install_requires=['rsa==3.4.2', 'requests==2.10.0'],
    tests_require=['fake-factory==0.5.7'],
    include_package_data=True
)
