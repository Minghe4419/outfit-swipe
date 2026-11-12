"""Copy app/ into docs/ for GitHub Pages main /docs publishing."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
for path in (root/'app').iterdir():
    if path.is_file():shutil.copy2(path,root/'docs'/path.name)
    elif path.is_dir():shutil.copytree(path,root/'docs'/path.name,dirs_exist_ok=True)
(root/'docs/.nojekyll').touch()
print('Pages output refreshed in docs/')
