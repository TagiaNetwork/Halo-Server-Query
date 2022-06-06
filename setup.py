import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HaloServerQuery",
    version="1.0.0",
    author="Tagia Network",
    author_email="tagianetwork@gmail.com",
    description="Query Halo Custom Edition servers for valuable information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TagiaNetwork/Halo-Server-Query",
    project_urls={
        "Bug Tracker": "https://github.com/TagiaNetwork/Halo-Server-Query/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
