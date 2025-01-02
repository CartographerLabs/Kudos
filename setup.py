
import setuptools

setuptools.setup(
    name="kudos",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=[
        "networkx",
        "filelock",
        "torch",
        "transformers",
        "jsonformer",
        "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "wargame-run=game.run_simulation:main"
        ]
    },
)
