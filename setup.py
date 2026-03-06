"""
Red WiFi setup.py
Package configuration for PyPI distribution.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="red-wifi",
    version="2.0.0",
    author="Red WiFi Contributors",
    author_email="contact@redwifi.dev",
    description="Professional WiFi Penetration Testing Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redwifi/red-wifi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: Communications",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "netaddr>=0.8.0",
        "colorama>=0.4.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "red-wifi=red_wifi.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
