from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SemanticShield',
    version='0.1.11',
    author='SemanticBrain',
    author_email='info@semanticbrain.net',
    description='SemanticShield library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SemanticBrainCorp/SemanticShield',
    project_urls = {
        "Bug Tracker": "https://github.com/SemanticBrainCorp/SemanticShield/issues"
    },
    license='MIT',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        "openai==1.40.6",
        "spacy==3.7.5",
        "Faker==25.9.2",
        "presidio-analyzer==2.2.355",
        "exrex==0.11.0",
        "better_profanity==0.7.0",
        "alt-profanity-check==1.5.1",
        "transformers==4.44.0",
        "torch==2.4.0"
        ],
)
