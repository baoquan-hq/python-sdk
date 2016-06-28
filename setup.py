from setuptools import setup, find_packages

setup(
    name='eagle-sdk',
    version='1.0.2',
    packages=find_packages(),
    url='https://github.com/baoquan-hq/python-sdk.git',
    license='gpl-3.0',
    author='sbwdlihao',
    author_email='sbwdlihao@gmail.com',
    keywords='baoquan eagle sdk',
    description='sdk for members to use the service of baoquan.com',
    install_requires=['rsa==3.4.2', 'requests==2.10.0'],
    tests_require=['fake-factory==0.5.7'],
    include_package_data=True
)
