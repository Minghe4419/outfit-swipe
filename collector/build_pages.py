"""Copy app/ into docs/ for GitHub Pages main /docs publishing."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
for path in (root/'app').iterdir():
    if path.is_file():shutil.copy2(path,root/'docs'/path.name)
(root/'docs/.nojekyll').touch()
print('Pages output refreshed in docs/')
