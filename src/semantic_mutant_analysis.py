# Disclosure: The code here is heavily inspired by:
# https://julien.danjou.info/finding-definitions-from-a-source-file-and-a-line-number-in-python/

import ast
import tokenize
import intervaltree


class SemanticMutantAnalysis:

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.changed_file_name = repo_path + "/example_class.py"
        self.changed_line_number = 15
        self.tree = intervaltree.IntervalTree()
        self.file_to_tree()

    def file_to_tree(self):
        with tokenize.open(self.changed_file_name) as f:
            parsed = ast.parse(f.read(), filename=self.changed_file_name)
        for node in ast.walk(parsed):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start, end = self.compute_interval(node)
                self.tree[start:end] = node

    def compute_interval(self, node):
        min_lineno = node.lineno
        max_lineno = node.lineno
        for node in ast.walk(node):
            if hasattr(node, "lineno"):
                min_lineno = min(min_lineno, node.lineno)
                max_lineno = max(max_lineno, node.lineno)
        return min_lineno, max_lineno + 1

    def query_line_number(self, line_number: int):
        matches = self.tree[line_number]
        if matches:
            return min(matches, key=lambda i: i.length()).data.name