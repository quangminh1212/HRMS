"""
Setup script for HRMS (Human Resource Management System).
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hrms",
    version="1.0.0",
    author="HRMS Development Team",
    author_email="dev@hrms.vn",
    description="Human Resource Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/hrms",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "pre-commit",
        ],
        "prod": [
            "gunicorn",
            "psycopg2-binary",
        ],
    },
    entry_points={
        "console_scripts": [
            "hrms=run:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
