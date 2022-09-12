# pip install -e .
# pip install -r requirements.txt
# use pip-compile to get stuff for requirements .txt (piptools)
# use pipreqs --force to get base packages (pipreqs)

# pip install alpaca-py  ## use for alpaca error
# python -m pip install mysql-connector-python   ## use if _version error is found
## probably try to refine so it works right away? Fix what libraries are used in requirements.txt? add some more folders in src?

# if the bot works with task scheduler start doing the algorithmic one and try to clean everything up so that it all works with one class
# and that there arent many files in one folder

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

