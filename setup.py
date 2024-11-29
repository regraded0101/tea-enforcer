from setuptools import setup, find_packages

setup(
    name='tea-enforcer',
    version='0.1.0',
    description='Pre-commit hook to check for Americanised spellings',
    author='Jon Fuller',
    author_email='jonfuller0207@mail.com',
    url='https://github.com/regraded0101/tea-enforcer',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
