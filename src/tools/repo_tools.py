import ast
import os
import subprocess
import tempfile
from typing import List, Optional, Dict
from git import Repo
import shutil

class RepoTools:
    @staticmethod
    def clone_repository(repo_url: str) -> str:
        """Clones a repository into a temporary directory and returns the path."""
        temp_dir = tempfile.mkdtemp()
        try:
            Repo.clone_from(repo_url, temp_dir)
            return temp_dir
        except Exception as e:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception(f"Failed to clone repository: {str(e)}")

    @staticmethod
    def get_git_log(repo_path: str) -> List[Dict]:
        """Returns the git log as a list of dictionaries."""
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
