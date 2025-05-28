from setup import setup, find_packages

setup(
    name='grocery_cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'grocery=grocery_cli.main:cli',
        ],
    },
)