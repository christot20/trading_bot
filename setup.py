# pip install -e .
# pip install -r requirements.txt
# use pip-compile to get stuff for requirements .txt
# use pipreqs --force to get base packages

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Palgo Bot',
    version='1.0',
    description='Python Algorithmic Trading Bot',
    long_description=readme,
    author='Thomas Christo',
    author_email='thomaschristo1234@yahoo.com',
    url='https://github.com/christot20/trading_bot',
    license=license,
    python_requires='>=3.10',
    packages=find_packages(exclude=('tests'))
)

