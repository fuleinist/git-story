from setuptools import setup, find_packages

setup(
    name="git-story",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "jinja2>=3.0",
        "requests>=2.28",
    ],
    entry_points={
        "console_scripts": [
            "git-story=gitstory.cli:main",
        ],
    },
)
