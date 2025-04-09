from setuptools import setup, find_packages

setup(
    name="obsidian-concierge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "pydantic>=1.8.2,<2.0.0",
        "openai>=1.0.0,<2.0.0",
        "sqlalchemy>=1.4.23,<1.5.0",
        "alembic>=1.7.3,<1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5,<7.0.0",
            "pytest-cov>=2.12.1,<3.0.0",
            "httpx>=0.18.2,<0.19.0",
            "black>=21.7b0,<22.0",
            "flake8>=3.9.2,<4.0.0",
            "mypy>=0.910,<1.0.0",
            "isort>=5.9.3,<6.0.0",
        ],
        "docs": [
            "mkdocs>=1.2.3,<2.0.0",
            "mkdocs-material>=7.3.2,<8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "obsidian-concierge=obsidian_concierge.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered assistant for managing and analyzing Obsidian notes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/obsidian-concierge",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
) 