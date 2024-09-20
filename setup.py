from setuptools import setup, find_packages

setup(
    name='myframework',
    version='0.1.0',
    description='An ultra-lightweight, dependency-free web framework in Python',
    author='Nishanta Parajuli',
    author_email='astroguy800@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    url='https://github.com/AstroGuy1/Flintor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
