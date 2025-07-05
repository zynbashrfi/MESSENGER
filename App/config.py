import pathlib

base_dir = pathlib.Path(__file__).resolve().parent.parent
db_path = base_dir / "messenger.db"