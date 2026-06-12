import os
import shutil
import stat
from pathlib import Path
import subprocess
import tomllib
from pathlib import Path
import glob
import yaml


def copy_file(path: str, source_folder: str, target_folder: str) -> None:
    """Copy file from a path in 'source_folder' to the same path inside 'target_folder'."""
    head, tail = os.path.split(path)
    if head:
        os.makedirs(target_folder + "\\" + head, exist_ok=True)
    shutil.copy(source_folder + path, target_folder + "\\" + head)


def copy_folder(path: str, source_folder: str, target_folder: str) -> None:
    """Copy folder from a path in 'source_folder' to the same path inside 'target_folder'."""
    shutil.copytree(source_folder + "\\" + path, target_folder + "\\" + path)


def create_zip_archive(source_folder: str, target_folder: str) -> str:
    """Create .zip file based on a folder.

    Args:
        source_folder (str): Path to source folder
        target_folder (str): Path to target folder (without .zip)

    Returns:
        str: filepath created
    """
    return shutil.make_archive(source_folder, "zip", target_folder)


def makedirs_overwrite(path: str):
    """Same as os.makedirs but overwrites existing dirs."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def handle_pip_install(pip_install_command: str) -> list[str]:
    """Executes 'pip install ...' commands and records installed, already satisfied and erroneous installations.

    Args:
        pip_install_command (str): Executed command

    Raises:
        Exception: When 'pip install ..' errors

    Returns:
        list[str]: names of the installed packages
    """ """"""
    out = get_ipython().getoutput(pip_install_command)
    installed = [l for l in out if "successfully installed" in l.lower()]
    satisfied = [l for l in out if "already satisfied" in l.lower()]
    errors = [l for l in out if "error" in l.lower()]

    if installed:
        print("✅", *installed)
    if errors:
        raise Exception("❌", *errors)
    if not installed and not errors:
        print(
            f"✔ All requirements already satisfied ({len(satisfied)} packages checked)"
        )
    return installed


def handle_restart_after_installing_packages(installed_packages) -> None:
    if installed_packages:
        print(
            "New packages have been installed. Kernel will shut down. Please restart (with correct virtual environment selected)."
        )
        os._exit(00)


def print_dependencies_using_pipdeptree(depth: int = 0) -> None:
    """Print dependencies of virtual environment using pipdeptree package in a format suitable for pyproject.toml files.

    Args:
        depth (int, optional): Depth of dependency tree. Defaults to 0.
    """
    deps = get_ipython().getoutput(
        "pipdeptree --depth $depth --freeze --exclude pip,setuptools,wheel"
    )
    formatted = "\n".join(f'  "{d.replace("==", ">=")}"' for d in deps)
    print("dependencies = [")
    print(formatted)
    print("]")


def print_requirements_and_create_txt_file_for_src_using_pipreqs(
    src: str = r"..\src", output_file: str = r"..\requirements.txt"
) -> None:
    """Print requirements (in a format suitable for pyproject.toml files) and create requirements.txt file for package under 'src'.

    Args:
        src (str, optional): path to package. Defaults to "..\\src".
        output_file (str, optional): requirements file created. Defaults to r"..\requirements.txt".
    """
    get_ipython().getoutput(f"pipreqs {src} --force --savepath {output_file}")
    deps = Path(output_file).read_text().splitlines()
    deps = [d.strip() for d in deps if d.strip()]  # remove empty lines

    print("dependencies = [")
    for d in deps:
        print(f'  "{d.replace("==", ">=")}",')
    print("]")


def print_requirements_and_create_txt_file_for_venv_using_pip_freeze() -> None:
    """
    Use 'pip freeze' command to create requirements file for entire virtual environment and print the dependencies in a format suitable for pyproject.toml files.
    """
    output_file = r"..\requirements_venv.txt"
    with open(output_file, "w") as f:
        subprocess.run(["pip", "freeze"], stdout=f, check=True)
    deps = Path(output_file).read_text().splitlines()
    deps = [d.strip() for d in deps if d.strip()]  # remove empty lines

    print("dependencies = [")
    for d in deps:
        print(f'  "{d.replace("==", ">=")}",')
    print("]")


def get_package_name(path_pyprojecttoml: str = "..\\pyproject.toml") -> str:
    """Get package name from pyproject.toml file.

    Args:
        path_pyprojecttoml (str, optional): path to pyproject.toml file. Defaults to "..\\pyproject.toml".

    Returns:
        str: package name
    """
    with open(path_pyprojecttoml, "rb") as f:
        data = tomllib.load(f)
    return data["project"]["name"]


def get_git_branch() -> str:
    """Get name of current branch in git.

    Returns:
        str: name
    """
    return subprocess.check_output(
        ["git", "branch", "--show-current"], text=True
    ).strip()


def clean_notebooks_in_folder(folder_path: str, skip: list[str] = []) -> None:
    """Clean all jupyter notebooks in a folder using 'nbstripout'.

    Args:
        folder_path (str): path to folder
        skip (list[str], optional): Notebook file names that are not cleaned. Defaults to [].
    """
    file_type = "*.ipynb"
    files = glob.glob(file_type, root_dir=folder_path)
    if not files:
        print(f"No {file_type} found in {os.path.abspath(folder_path)}")
    else:
        print(f"Cleaning notebooks: {files}")
    for file in files:
        if not file in skip:
            print(subprocess.run(f"nbstripout {folder_path + "//" + file}".split(" ")))


def convert_jupyter_notebooks_in_folder_to_quarto(folder_path: str) -> None:
    """Copy and convert all jupyter notebooks in a folder to quarto (.qmd).
    Skips conversion if an existing .qmd file is newer than the .ipynb file.

    Args:
        folder_path (str): path of folder
    """
    file_type = "*.ipynb"
    files = glob.glob(file_type, root_dir=folder_path)

    if not files:
        print(f"No {file_type} found in {os.path.abspath(folder_path)}")
        return

    print(f"Found: {files}")

    for file in files:
        ipynb_path = Path(folder_path) / file
        qmd_path = Path(folder_path) / (Path(file).stem + ".qmd")

        # Check if .qmd exists and is newer than .ipynb
        if qmd_path.exists():
            ipynb_mtime = ipynb_path.stat().st_mtime
            qmd_mtime = qmd_path.stat().st_mtime
            if qmd_mtime > ipynb_mtime:
                print(f"⏭ Skipping {file} — .qmd is newer than .ipynb")
                continue

        print(f"Converting {file} → {qmd_path.name}")
        result = subprocess.run(
            ["quarto", "convert", str(ipynb_path)], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ Converted {file}")
        else:
            print(f"❌ Failed to convert {file}: {result.stderr}")


def sync_jupyter_and_quarto_in_folder(folder_path: str) -> None:
    """Sync jupyter notebooks and quarto files in a folder by converting
    whichever file format was modified most recently.

    Args:
        folder_path (str): path of folder
    """
    folder = Path(folder_path)

    ipynb_files = {f.stem: f for f in folder.glob("*.ipynb")}
    qmd_files = {f.stem: f for f in folder.glob("*.qmd")}

    # All unique stems across both formats
    all_stems = set(ipynb_files.keys()) | set(qmd_files.keys())

    for stem in all_stems:
        ipynb_path = ipynb_files.get(stem)
        qmd_path = qmd_files.get(stem)

        # Only .ipynb exists → convert to .qmd
        if ipynb_path and not qmd_path:
            print(f"🔄 {stem}: .ipynb only → converting to .qmd")
            _quarto_convert(ipynb_path)

        # Only .qmd exists → convert to .ipynb
        elif qmd_path and not ipynb_path:
            print(f"🔄 {stem}: .qmd only → converting to .ipynb")
            _quarto_convert(qmd_path)

        # Both exist → convert based on which is newer
        else:
            ipynb_mtime = ipynb_path.stat().st_mtime
            qmd_mtime = qmd_path.stat().st_mtime

            if ipynb_mtime > qmd_mtime:
                print(f"🔄 {stem}: .ipynb is newer → converting to .qmd")
                _quarto_convert(ipynb_path)
            elif qmd_mtime > ipynb_mtime:
                print(f"🔄 {stem}: .qmd is newer → converting to .ipynb")
                _quarto_convert(qmd_path)
            else:
                print(f"✔ {stem}: both files are in sync")


def _quarto_convert(file_path: Path) -> None:
    """Run quarto convert on a file and report the result.

    Args:
        file_path (Path): path to the file to convert
    """
    result = subprocess.run(
        ["quarto", "convert", str(file_path)], capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✅ Converted {file_path.name}")
    else:
        print(f"  ❌ Failed to convert {file_path.name}: {result.stderr}")


def convert_quarto_notebooks_in_folder_to_jupyter(folder_path: str) -> None:
    """Copy and convert all quarto notebooks (.qmd) in a folder to jupyter (.ipynb).

    Args:
        folder_path (str): path of folder
    """
    file_type = "*.qmd"
    files = glob.glob(file_type, root_dir=folder_path)
    if not files:
        print(f"No {file_type} found in {os.path.abspath(folder_path)}")
    else:
        print(f"Converting: {files}")
    for file in files:
        print(subprocess.run(f"quarto convert {folder_path + "//" + file}".split(" ")))


def create_directory(path: str, overwrite: bool = True) -> None:
    """Create directory or clear files in directory if it exists already.

    Args:
        path (str): path of directory
        overwrite (bool): If true, existing directories are overwritten (cleared). Defaults to True.
    """
    if os.path.exists(path):
        if overwrite:
            shutil.rmtree(path, onexc=force_remove)
            os.makedirs(path)
    else:
        os.makedirs(path)


def force_remove(func, path, exc):
    """
    Forced removal of file (remove read-only flag and retry).

    Used as in 'shutil.rmtree(target_folder, onerror=force_remove)'.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def merge_remote_branch(remote: str = "origin", branch: str = "main") -> None:
    """Merge a remote branch into the current branch and check for conflicts.

    Args:
        remote (str): remote name (default: "origin")
        branch (str): branch name to merge from (default: "main")
    """
    # Fetch latest from remote
    print(f"Fetching {remote}...")
    fetch = subprocess.run(["git", "fetch", remote], capture_output=True, text=True)
    if fetch.returncode != 0:
        print(f"❌ Fetch failed: {fetch.stderr}")
        return
    print(f"✅ Fetched {remote}")

    # Attempt merge
    print(f"Merging {remote}/{branch}...")
    merge = subprocess.run(
        ["git", "merge", f"{remote}/{branch}"], capture_output=True, text=True
    )

    if merge.returncode == 0:
        print(f"✅ Merged {remote}/{branch} successfully")
        print(merge.stdout)
        return

    # Check for conflicts
    conflicts = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True,
        text=True,
    )
    conflicted_files = conflicts.stdout.strip().splitlines()


def convert_meeting_minutes_to_quarto(root_folder: str) -> None:
    """Convert meeting minutes from .docx to .qmd using pandoc.

    - Subfolder names are used as the title of the .qmd file
    - .qmd files are created in the root folder (not in subfolders)
    - Media files are extracted to a dedicated media subfolder
    - Additional files in subfolders are linked as supporting documents

    Args:
        root_folder (str): path to the folder containing the minute subfolders

    **Expected folder structure:**
    ```
    docs/minutes/
    ├── 2024-01-15 Kickoff Meeting/
    │   ├── minutes.docx
    │   ├── agenda.pdf
    │   └── presentation.pptx
    ├── 2024-02-10 Status Update/
    │   ├── minutes.docx
    │   └── budget.xlsx
    ```

    **Output:**
    ```
    docs/minutes/
    ├── 2024-01-15 Kickoff Meeting/       ← subfolders unchanged
    │   ├── minutes.docx
    │   ├── agenda.pdf
    │   └── presentation.pptx
    ├── 2024-02-10 Status Update/
    │   ├── minutes.docx
    │   └── budget.xlsx
    ├── 2024-01-15 Kickoff Meeting.qmd    ← generated .qmd files
    ├── 2024-02-10 Status Update.qmd

    """
    root = Path(root_folder)

    for subfolder in sorted(root.iterdir()):
        if not subfolder.is_dir():
            continue

        # Find .docx files in the subfolder
        docx_path = subfolder / "minutes.docx"
        if not docx_path.exists():
            print(f"⏭ Skipping {subfolder.name} — no minutes.docx found")
            continue

        # Use subfolder name as title
        title = subfolder.name
        qmd_path = root / f"{title}.qmd"
        media_dir = root / f"{title}-media"  # dedicated media folder

        # Convert .docx to markdown using pandoc with media extraction
        # docx_path = docx_files[0]
        print(f"🔄 Converting {docx_path.name} → {qmd_path.name}")
        print(docx_path)
        result = subprocess.run(
            [
                "pandoc",
                str(docx_path),
                "-t",
                "markdown",
                f"--extract-media={media_dir}",  # extract media to dedicated folder
                "--lua-filter=clear_image_captions.lua",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"❌ Failed to convert {docx_path.name}: {result.stderr}")
            continue

        # Check if any media was extracted
        media_files = list(media_dir.rglob("*")) if media_dir.exists() else []
        media_files = [f for f in media_files if f.is_file()]
        if media_files:
            print(
                f"  📎 Extracted {len(media_files)} media file(s) to {media_dir.name}/"
            )

        # Fix media paths in markdown — pandoc uses absolute paths, make them relative
        markdown_content = result.stdout
        markdown_content = markdown_content.replace(str(media_dir), f"{title}-media")
        # Also fix Windows backslashes in paths
        markdown_content = markdown_content.replace(
            str(media_dir).replace("\\", "/"), f"{title}-media"
        )

        # Find supporting documents (all non-.docx files in subfolder)
        supporting_files = [
            f
            for f in subfolder.iterdir()
            if f.is_file() and f.suffix.lower() != ".docx"
        ]

        # Build .qmd content
        content = f"""---
title: "{title}"
---

{markdown_content}
"""

        # Append supporting documents section
        if supporting_files:
            content += "\n# Supporting Documents\n\n"
            for f in sorted(supporting_files):
                relative_path = f.relative_to(root)
                # Use forward slashes for Quarto compatibility
                relative_path_str = str(relative_path).replace("\\", "/")
                content += f"- [{f.name}]({relative_path_str})\n"

        # Write .qmd file
        qmd_path.write_text(content, encoding="utf-8")
        print(f"✅ Created {qmd_path.name}")

    update_minutes_sidebar("..//_quarto.yml", "..//docs//minutes")


def update_minutes_sidebar(quarto_yml_path: str, minutes_folder: str) -> None:
    """Update the Minutes sidebar in _quarto.yml with all .qmd files.
    overview.qmd is listed first, paths are relative to the project root.

    Args:
        quarto_yml_path (str): path to _quarto.yml
        minutes_folder (str): path to the minutes folder
    """
    minutes_path = Path(minutes_folder)

    # Get all .qmd files, separate overview from the rest
    all_files = sorted(minutes_path.glob("*.qmd"))
    overview = [f for f in all_files if f.stem.lower() == "overview"]
    rest = [f for f in all_files if f.stem.lower() != "overview"]

    # Build entries without leading "..\" and with forward slashes
    def to_entry(f: Path) -> str:
        return str(f).replace("\\", "/").lstrip("./")

    entries = [to_entry(f) for f in overview + rest]

    with open(quarto_yml_path, "r") as f:
        config = yaml.safe_load(f)

    # Find and update the Minutes sidebar
    for sidebar in config["website"]["sidebar"]:
        if sidebar.get("title") == "Minutes":
            sidebar["contents"] = entries
            break

    with open(quarto_yml_path, "w") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"✅ Updated Minutes sidebar with {len(entries)} files:")
    for e in entries:
        print(f"  - {e}")
