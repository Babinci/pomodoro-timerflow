import requests
import yaml
import urllib.parse
from typing import List

# Load secrets (assuming you have a .secrets.yaml file)
# with open(".secrets.yaml", "r") as file:
#     secrets = yaml.safe_load(file)
# git_token = secrets["env"]["GIT"]
git_token = ""


def count_tokens(text: str) -> int:
    tokens = text.split()
    return len(tokens)


def build_yaml_tree(include_dirs: List[str], include_files: List[str]) -> dict:
    """
    Build a nested dictionary representing the file hierarchy for the YAML string.

    Args:
        include_dirs (list): List of directories to include (all contents recursively).
        include_files (list): List of specific file paths to include.

    Returns:
        dict: Nested dictionary representing the file tree.
    """
    tree = {}
    for dir_path in include_dirs:
        parts = dir_path.split("/")
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
        current.clear()  # Ensure directory is an empty dict {}

    for file_path in include_files:
        parts = file_path.split("/")
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif current[part] is None:
                raise ValueError(f"Cannot add file under a file: {file_path}")
            current = current[part]
        if parts[-1] in current and current[parts[-1]] == {}:
            raise ValueError(f"Cannot add file when directory is included: {file_path}")
        current[parts[-1]] = None
    return tree


def filter_response(
    response_text: str,
    include_dirs: List[str],
    include_files: List[str],
    exclude_dirs: List[str],
) -> str:
    """
    Filter the API response to include specified files and directories while excluding specified folders.

    Args:
        response_text (str): The raw response text from the API.
        include_dirs (list): List of directories to include.
        include_files (list): List of specific files to include.
        exclude_dirs (list): List of directories to exclude.

    Returns:
        str: Filtered response text.
    """
    lines = response_text.splitlines()

    # Separate directory tree and file contents
    for i, line in enumerate(lines):
        if line.startswith("/"):
            break
    else:
        i = len(lines)

    tree_lines = lines[:i]
    content_lines = lines[i:]

    # **Filter Directory Tree**
    filtered_tree_lines = []
    skip_depth = -1
    path_stack = []

    for line in tree_lines:
        depth = (len(line) - len(line.lstrip())) // 4  # Calculate indentation level
        item_name = line.strip().split(" ", 1)[-1].strip()  # Extract folder/file name
        while len(path_stack) > depth:
            path_stack.pop()
        full_path = "/" + "/".join(path_stack + [item_name])

        if depth <= skip_depth:
            skip_depth = -1  # Stop skipping when returning to a higher level

        if skip_depth == -1:
            excluded_paths = ["/" + dir for dir in exclude_dirs]
            if any(
                full_path.startswith(ex_path + "/") or full_path == ex_path
                for ex_path in excluded_paths
            ):
                skip_depth = depth  # Start skipping this folder and its subcontents
            else:
                filtered_tree_lines.append(line)
                if depth < len(path_stack):
                    path_stack[depth] = item_name
                else:
                    path_stack.append(item_name)

    directory_tree = "\n".join(filtered_tree_lines) + "\n"

    # **Parse and Filter File Contents**
    file_sections = []
    current_path = None
    current_content = []
    for line in content_lines:
        if line.startswith("/"):
            if current_path:
                file_sections.append((current_path, "\n".join(current_content)))
            current_path = line.rstrip(":")
            current_content = []
        elif (
            line.strip()
            == "--------------------------------------------------------------------------------"
        ):
            continue
        else:
            current_content.append(line)
    if current_path:
        file_sections.append((current_path, "\n".join(current_content)))

    # Define allowed and excluded prefixes
    allowed_prefixes = ["/" + dir + "/" for dir in include_dirs]
    allowed_files = ["/" + file for file in include_files]
    excluded_prefixes = ["/" + dir + "/" for dir in exclude_dirs]

    # Filter file sections
    filtered_sections = []
    for path, content in file_sections:
        if (
            any(path.startswith(prefix) for prefix in allowed_prefixes)
            or path in allowed_files
        ) and not any(path.startswith(ex_prefix) for ex_prefix in excluded_prefixes):
            filtered_sections.append(
                f"{path}:\n--------------------------------------------------------------------------------\n{content}\n--------------------------------------------------------------------------------"
            )

    # Combine filtered directory tree and file contents
    filtered_response = directory_tree + "\n".join(filtered_sections)
    return filtered_response


def save_llm_context(
    base_url: str,
    include_dirs: List[str] = None,
    include_files: List[str] = None,
    exclude_dirs: List[str] = None,
    api_key: str = None,
    llm_context_file: str = "prompts/llm_context.md",
):
    """
    Fetch repository contents from UIThub API, filter based on inclusions and exclusions, and save to a file.

    Args:
        base_url (str): Base URL with branch (e.g., "https://uithub.com/owner/repo/tree/master").
        include_dirs (list, optional): List of directories to include.
        include_files (list, optional): List of specific files to include.
        exclude_dirs (list, optional): List of directories to exclude.
        api_key (str, optional): GitHub API key for authentication.
        llm_context_file (str): File path to save the context (default: "prompts/llm_context.md").
    """
    params = {}
    if include_dirs or include_files:
        tree = build_yaml_tree(include_dirs or [], include_files or [])
        yaml_string = yaml.dump(tree, default_flow_style=False)
        encoded_yaml = urllib.parse.quote(yaml_string)
        params["yamlString"] = encoded_yaml
    if api_key:
        params["apiKey"] = api_key

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        filtered_response = filter_response(
            response.text, include_dirs or [], include_files or [], exclude_dirs or []
        )
        with open(llm_context_file, "w", encoding="utf-8") as f:
            f.write(filtered_response)
        print(f"Filtered context saved to {llm_context_file}")
        token_count = count_tokens(filtered_response)
        print(f"Token count: {token_count}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# **Example Usage**
base_url = "https://uithub.com/Babinci/pomodoro-timerflow/tree/master"
folders_to_choose = [
    "backend",
    "memory-bank",
]
files_to_choose = ["Dockerfile", "restart_docker.sh"]
exclude_dirs = []  # Folders to exclude
git_bearer = git_token
llm_context_file = "prompts/llm_context.md"

save_llm_context(
    base_url,
    include_dirs=folders_to_choose,
    include_files=files_to_choose,
    exclude_dirs=exclude_dirs,
    api_key=None,
    llm_context_file=llm_context_file,
)
