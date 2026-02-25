import ast
import os
import subprocess
import tempfile
from typing import List, Optional, Dict
import shutil
try:
    from git import Repo
    HAS_GIT_PYTHON = True
except (ImportError, Exception):
    HAS_GIT_PYTHON = False

class RepoTools:
    @staticmethod
    def clone_repository(repo_url: str) -> str:
        """Clones a repository into a temporary directory and returns the path."""
        temp_dir = tempfile.mkdtemp()
        
        # Try Git first
        if HAS_GIT_PYTHON:
            try:
                Repo.clone_from(repo_url, temp_dir)
                return temp_dir
            except Exception as e:
                print(f"Git clone failed: {str(e)}. Attempting fallback...")
        
        # Fallback for GitHub Repos if Git is missing/broken
        if "github.com" in repo_url:
            try:
                # Normalize URL for zip download
                zip_url = repo_url.rstrip("/") + "/archive/refs/heads/main.zip"
                zip_path = os.path.join(tempfile.gettempdir(), f"repo_{os.path.basename(temp_dir)}.zip")
                
                print(f"Downloading repository zip from {zip_url}...")
                subprocess.run(["curl", "-L", zip_url, "-o", zip_path], check=True, capture_output=True)
                
                print("Extracting repository content...")
                subprocess.run(["unzip", "-q", zip_path, "-d", temp_dir], check=True, capture_output=True)
                
                # unzip usually creates a nested directory
                contents = os.listdir(temp_dir)
                if len(contents) == 1 and os.path.isdir(os.path.join(temp_dir, contents[0])):
                    nested_path = os.path.join(temp_dir, contents[0])
                    # Move everything up
                    for item in os.listdir(nested_path):
                        shutil.move(os.path.join(nested_path, item), os.path.join(temp_dir, item))
                    os.rmdir(nested_path)
                
                os.remove(zip_path)
                return temp_dir
            except Exception as e:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                raise Exception(f"Failed to clone repository (both git and fallback failed): {str(e)}")
        else:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception("Git is not available and no fallback for this URL type is implemented.")

    @staticmethod
    def get_git_log(repo_path: str) -> List[Dict]:
        """Returns the git log as a list of dictionaries."""
        if HAS_GIT_PYTHON:
            try:
                repo = Repo(repo_path)
                commits = list(repo.iter_commits())
                return [
                    {
                        "hash": commit.hexsha,
                        "message": commit.message.strip(),
                        "author": commit.author.name,
                        "date": commit.committed_datetime.isoformat(),
                    }
                    for commit in reversed(commits)
                ]
            except Exception:
                pass
        
        # Fallback if git log is unavailable
        return [{
            "hash": "unknown",
            "message": "Commit history unavailable (downloaded via zip fallback)",
            "author": "System",
            "date": "2024-01-01T00:00:00"
        }]

    @staticmethod
    def analyze_graph_structure(repo_path: str) -> Dict:
        """Analyzes the repository for LangGraph StateGraph instantiation using AST."""
        results = {
            "stategraph_found": False,
            "parallel_execution": False,
            "nodes": [],
            "edges": [],
            "code_snippets": []
        }
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        try:
                            tree = ast.parse(f.read())
                            for node in ast.walk(tree):
                                # Look for StateGraph instantiation
                                if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "StateGraph":
                                    results["stategraph_found"] = True
                                
                                # Look for add_edge calls
                                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_edge":
                                    results["edges"].append(ast.unparse(node))
                                    
                                # Look for parallel patterns (very basic heuristic)
                                # A better heuristic would be checking if multiple edges originate from the same node
                        except Exception:
                            continue
        return results

    @staticmethod
    def list_files(repo_path: str) -> List[str]:
        """Lists all files in the repository."""
        file_list = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                file_list.append(rel_path)
        return file_list

    @staticmethod
    def read_file(repo_path: str, rel_path: str) -> Optional[str]:
        """Reads a file from the repository."""
        full_path = os.path.join(repo_path, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                return f.read()
        return None
