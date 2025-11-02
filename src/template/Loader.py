from pathlib import Path
from utils import get_project_root
from .Template import Template  # your Template class

class TemplateLoader:
    """
    Looks for templates under the project root / assets directory.
    """

    def __init__(self, search_dir=None):
        # Default to `assets/pages` under the project root
        root = get_project_root()
        self.search_dir = Path(search_dir or (root / "assets"))

    def load(self, template_name: str):
        """
        Load and parse a template by name.
        e.g. 'pages/main.html' -> assets/pages/main.html
        """
        path = self.search_dir / template_name

        if not path.is_file():
            raise FileNotFoundError(f"Template not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Return a Template instance ready to render
        return Template(content)
