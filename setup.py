import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutormfe_extensions", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-mfe-extensions",
    version=ABOUT["__version__"],
    url="https://github.com/edunext/tutor-contrib-mfe-extensions",
    project_urls={
        "Code": "https://github.com/edunext/tutor-contrib-mfe-extensions",
        "Issue tracker": "https://github.com/edunext/tutor-contrib-mfe-extensions/issues",
    },
    license="AGPLv3",
    author="Moisés González",
    description="mfe_extensions plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=17.0.2", "tutor-mfe>=17.0.1"],
    entry_points={
        "tutor.plugin.v1": [
            "mfe_extensions = tutormfe_extensions.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
