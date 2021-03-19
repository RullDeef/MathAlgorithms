import setuptools

setuptools.setup(
    name="normal-algorifms",
    version="0.0.1",
    author="Rull Deef",
    author_email="deeroll666@gmail.com",
    license="MIT",
    description="simple normal algorifm executor",
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RullDeef/MarkovAlgorifms",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points="""
[console_scripts]
nalg = normalg.executor:main
"""
)
