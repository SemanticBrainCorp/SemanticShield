from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='shield',
    version='0.0.1',
    author='SemanticBrain',
    author_email='albert.r@semanticbrain.net',
    description='SemanticShield library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/albertsemantic/shield',
    project_urls = {
        "Bug Tracker": "https://github.com/albertsemantic/shield/issues"
    },
    license='proprietary',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=["openai==0.28.0","langchain==0.0.287","spacy==3.6.1","Faker==19.6.1","presidio-analyzer==2.2.33","exrex==0.11.0"],
)
