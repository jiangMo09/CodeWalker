import os
import shutil
import re
import requests
from fastapi import HTTPException

from git import Repo
from typing import Set


def clone_repo(repo_url: str, temp_dir: str) -> None:
    EXCLUDE_SET: Set[str] = {
        ".git",
        ".vscode",
        ".env",
        ".venv",
        "env",
        "venv",
        "ENV",
        "env.bak",
        "venv.bak",
        "myenv",
        ".DS_Store",
        "__pycache__",
    }

    # Repo.clone_from(repo_url, temp_dir)
    try:
        Repo.clone_from(repo_url, temp_dir)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to clone repository: {str(e)}"
        )

    def remove_excluded_items(directory: str) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.name in EXCLUDE_SET:
                    path = entry.path
                    if entry.is_dir():
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                elif entry.is_dir():
                    remove_excluded_items(entry.path)

    remove_excluded_items(temp_dir)

    print(f"倉庫已克隆到 {temp_dir}，並排除了指定的文件和目錄。")


def extract_github_info(repo_url):
    print(repo_url)
    patterns = [
        r"https://github\.com/([^/]+)/([^/]+)(?:\.git)?$",
        r"git@github\.com:([^/]+)/([^/]+)\.git$",
    ]

    for pattern in patterns:
        match = re.match(pattern, repo_url)
        if match:
            return match.group(1), match.group(2)

    return None, None


def is_public_repo(repo_url):
    response = requests.get(repo_url)
    return response.status_code == 200


def validate_repo_contents(temp_dir):
    allowed_extensions = {".html", ".js", ".css"}
    has_index_html = False

    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file == "index.html" and root == temp_dir:
                has_index_html = True
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in allowed_extensions:
                return False

    return has_index_html
