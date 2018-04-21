import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel("apistar_cors_hooks.py"), "r") as f:
    version_marker = "__version__ = "
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip('"')
            break
    else:
        raise RuntimeError("Version marker not found.")


setup(
    name="apistar_cors_hooks",
    url='https://github.com/lucianoratamero/apistar_cors_hooks',
    author='Luciano Ratamero',
    author_email='luciano@ratamero.com',
    version=version,
    description="CORS support for API Star via event hooks.",
    long_description="https://github.com/lucianoratamero/apistar_cors_hooks",
    packages=[],
    py_modules=["apistar_cors_hooks"],
    install_requires=[
        "apistar>=0.4",
        "wsgicors>=0.7,<0.8",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
