import setuptools
from pathlib import Path


with open(Path(__file__).parent/"README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fund-analyser",
    version="1.0",
    author="M. Deniz Kizilirmak",
    author_email="kizilirmakmd@gmail.com",
    description="Analyser for funds in tefas.gov.tr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dn1z/fund_analyser",
    packages=["fund_analyser"],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': ['fund_analyser = fund_analyser:main']
    },
)