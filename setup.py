from setuptools import setup, find_packages
from pathlib import Path

this_directory: Path = Path(__file__).parent.absolute()
read_me = Path("README.md")
with read_me.open() as f:
    long_description = f.read()

setup(
    name="RPSLife",
    version="0.0.1",
    author="Jason Duncan",
    author_email="jason.matthew.duncan@gmail.com",
    description="A simple sim game of rock, paper, sicssors",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jduncan8142/RPSLife",
    project_urls={
        "Bug Tracker": "https://github.com/jduncan8142/RPSLife/issues",
        "Documentation": "https://github.com/jduncan8142/RPSLife/wiki"
    },
    packages=find_packages(where="RPSLife"),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English", 
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Games/Entertainment :: Simulation",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pygame==2.1.2"
    ], 
    package_data={'RPSLife': ['images/*.*', 'music/*.mp3']},
    entry_points={
        'console_scripts': [
            'RPSLife = RPSLife.main:rps_life',
        ],
    },
)
