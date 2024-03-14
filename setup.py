from setuptools import setup, find_packages

setup(
    name='BW',
    version='0.1',
    packages=find_packages(),
    description='Kuvaus projektista',
    author='Sinun nimesi',
    author_email='sinun.sahkopostisi@example.com',
    url='https://github.com/BWINB/BW',
    install_requires=[
        'matplotlib',
        'numpy',
        'ezdxf',
        'openpyxl',
        'reportlab',
        'transformers',
        'PyPDF2',
        'PyPDF4',
        'pikepdf',
    ],
)
