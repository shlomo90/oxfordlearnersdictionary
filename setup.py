import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dictionary-pkg-jaehwan",
    version="0.0.1",
    author="jaehwan",
    author_email="shlomolim90@gmail.com",
    description="Dictionaries for shell.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shlomo90/oxfordlearnersdictionary",
    #find_packages finds automatically packages we use
    packages=setuptools.find_packages(),
    install_requires=["requests", "BeautifulSoup"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
