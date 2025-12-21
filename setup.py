import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-search-python",
    version="1.6.8",  # Bug fixes: Video ID extraction, Transcript handling, ChannelSearch parsing, Comments continuation, Suggestions JSON parsing, and async Playlist initialization
    author="CertifiedCoders (forked from Hitesh Kumar Saini)",
    license='MIT',
    author_email="rajnishmishraaa1@gmail.com",
    description="Search for YouTube content without YouTube Data API v3. Maintained fork with modern Python support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CertifiedCoders/youtube-search-python",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'httpx>=0.28.1'  # compatible with httpx 0.28+
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Python 3.6 is EOL, updated to 3.7+
)