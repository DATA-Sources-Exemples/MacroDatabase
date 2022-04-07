import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="macrodatabase",
    packages=["macrodatabase"],
    version="1.0.0",
    license="MIT",
    description="This is a macro database of 570.000+ data series containing International Data (150+ countries), "
                "Interest Rates, Inflation, Monetary Data, U.S. (regional) data, Commodities, Real Estate and so "
                "much more. U.S. States and Countries curation is also included.",
    author="JerBouma",
    author_email="jer.bouma@gmail.com",
    url="https://github.com/JerBouma/MacroDatabase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["macroeconomics", "database", "fred"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
)
