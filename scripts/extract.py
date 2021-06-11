import pathlib
import shutil
import subprocess
import os

SOURCE_DIR = pathlib.Path(__file__).parents[1].absolute() / "nr_common"
TARGET_DIR = pathlib.Path("/tmp/nr-schemas")


def get_schemas(package_dir=SOURCE_DIR):
    jsonschema_dir = package_dir / "jsonschemas"
    mappings_dir = package_dir / "mappings"
    mapping_includes_dir = package_dir / "mapping_includes"
    return {
        "jsonschemas": (list(jsonschema_dir.glob('**/*.json'))),
        "mappings": (list(mappings_dir.glob('**/*.json'))),
        "mapping_includes": (list(mapping_includes_dir.glob('**/*.json')))
    }


def clone_schema_repo():
    os.chdir(str(SOURCE_DIR / ".."))
    subprocess.call(["pwd"])
    subprocess.call("./scripts/clone.sh")


def copy_schemas():
    target_dir = pathlib.Path("/tmp/nr-schemas")
    target_dirs = {
        "jsonschemas": target_dir / "jsonschemas",
        "mappings": target_dir / "mappings",
        "mapping_includes": target_dir / "mapping_includes",
    }
    for x in target_dirs.values():
        if not x.is_dir():
            x.mkdir(parents=True)
    source_dirs = get_schemas()
    for k, v in source_dirs.items():
        for source_path in v:
            print(str(source_path), str(target_dirs[k]))
            shutil.copy(str(source_path), str(target_dirs[k]))


def git_push():
    os.chdir(str(SOURCE_DIR / ".."))
    print("Git push path")
    subprocess.call(["pwd"])
    subprocess.call(["./scripts/push.sh", str(TARGET_DIR)])


if __name__ == '__main__':
    clone_schema_repo()
    copy_schemas()
    git_push()
