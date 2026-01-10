from setuptools import setup, find_packages

setup(
    name="sniperhire",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "jinja2",
        "pydantic",
        "groq",  
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "sniperhire=cli.cli:app",
        ],
    },
    author="Onari Alu",
    description="An AI-powered resume tailoring tool.",
    python_requires=">=3.9",
)
