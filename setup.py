from pathlib import Path
from shutil import copytree

from setuptools import setup
from setuptools.command.build_py import build_py as build_py_command


ROOT = Path(__file__).parent
REQUIREMENTS = [
    line.strip()
    for line in (ROOT / "requirements.txt").read_text().splitlines()
    if line.strip() and not line.lstrip().startswith("#") and not line.startswith("pytest")
]


class build_py(build_py_command):
    def run(self):
        super().run()
        for directory in ("static", "templates"):
            copytree(
                ROOT / directory,
                Path(self.build_lib) / directory,
                dirs_exist_ok=True,
            )


setup(
    name="flask-contact-api",
    version="2.1.1",
    description="A Flask contact and inventory application",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    py_modules=["app"],
    install_requires=REQUIREMENTS,
    cmdclass={"build_py": build_py},
)
