from setuptools import setup, find_packages

setup(
    name='comm_engineering',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.0',
        'scipy>=1.5.0',
        'matplotlib>=3.3.0',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for communication engineering simulation and engineering.',
    url='https://github.com/yourusername/comm_engineering',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)