import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepdrr",
    version="1.1.3",
    author="Benjamin D. Killeen",
    author_email="killeen@jhu.edu",
    description="A Catalyst for Machine Learning in Fluoroscopy-guided Procedures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[  # TODO: this needs to be updated
        "numpy",  # ==1.24.4 why?
        "torch",
        "torchvision",
        "nibabel",
        "scikit-image",
        "pydicom",
        "scipy",
        "pyvista",
        "pynrrd",
        "rich",
        "opencv-python",
        "seaborn",
        "graphviz",
        "pyglet>=1.4.11",
        "PyOpenGL>=3.1.7",
        "PyOpenGL_accelerate>=3.1.7",
        "trimesh",
        "pyrender @ git+https://github.com/liamjwang/pyrender.git@master",  # pyrender without hard PyOpenGL version requirement, TODO replace this when new version is released
        "killeengeo",
        "strenum",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "trame",
            "ipykernel",
            "ipywidgets",
        ],
        "cuda102": ["cupy-cuda102", "cuda-python>=10.2"],
        "cuda110": ["cupy-cuda110", "cuda-python>=11.0"],
        "cuda111": ["cupy-cuda111", "cuda-python>=11.1"],
        "cuda11x": ["cupy-cuda11x", "cuda-python>=11.0"],
        "cuda12x": ["cupy-cuda12x", "cuda-python>=12.0"],
},
    include_package_data=True,
    python_requires=">=3.7",
)
