import sys
from pathlib import Path

sys.path.insert(
    0, str((Path(__file__).parent.parent.parent / "src").resolve())
)

project = "Snakia"
copyright = "2025, RuJect"
author = "RuJect"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autosummary_generate = True
autosummary_imported_members = True

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "special-members": "__init__",
    "inherited-members": True,
    "show-inheritance": True,
}

templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
