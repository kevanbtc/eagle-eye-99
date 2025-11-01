from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="eagle_eye_estimator",
    version=version,
    description="Eagle Eye Estimator - Frappe app (assemblies, catalogs, estimate v2)",
    author="Eagle Eye",
    author_email="dev@eagleeye.local",
    license="GPL-3.0-or-later",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "frappe>=14",
    ],
)
