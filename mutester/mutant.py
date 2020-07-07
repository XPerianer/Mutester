from dataclasses import dataclass
from git import Repo
from unidiff import PatchSet

import re

from mutester.semantic_mutant_analysis import SemanticMutantAnalysis


@dataclass
class Mutant:
    mutant_id: int = -1
    modified_file_path: str = ""
    line_number_changed: int = -1
    previous_line: str = ""
    current_line: str = ""
    repo_path: str = ""
    modified_method: str = ""

    contains_loop: bool = None
    contains_branch: bool = None
    contains_math_operands: bool = None

    @classmethod
    def from_repo(cls, repo: Repo, mutant_id: int = None):
        current_diff = repo.index.diff(None)
        diff = repo.git.diff(repo.head, None, '--unified=0')
        patchset = PatchSet(diff)

        modified_file_path = patchset[0].target_file[2:]  # Remove "b/" from the path
        changed_sourcecode_line = patchset[0][0].source_start
        previous_line = ''
        for line in patchset[0][0]:
            if line.is_added:
                current_line = str(line)[2:]
            if line.is_removed:
                current_line = str(line)[2:]

        mutant = Mutant(mutant_id=mutant_id, modified_file_path=modified_file_path,
                      line_number_changed=changed_sourcecode_line,
                      previous_line=previous_line,
                      current_line=current_line, repo_path=repo.working_dir)
        mutant.modified_method = SemanticMutantAnalysis(mutant).method_name()

        regex_diff = repo.git.diff(repo.head, None, '--unified=7')
        mutant.context_analysis(regex_diff)

        return mutant

    # TODO: Refactor to a common static version?
    def context_analysis(self, string: str):
        self.contains_branch = re.search("if|else|switch", string) != None
        self.contains_loop = re.search("for|while", string) != None
        self.contains_math_operands = re.search("[-+*/]", string) != None
        self.contains_equality_comparison = re.search("==|is", string) != None

