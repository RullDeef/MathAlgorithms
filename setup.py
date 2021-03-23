import setuptools

setuptools.setup(
    name="math-algorithm-models",
    version="0.0.1",
    author="Rull Deef",
    author_email="deeroll666@gmail.com",
    license="MIT",
    description="simple algorithms executor",
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RullDeef/MarkovAlgorifms",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    entry_points={"console_scripts": ["matalg=matalg.executor:main"]},
    # setup_requires=["pytest-runner"],
    # tests_require=["pytest"]
)
