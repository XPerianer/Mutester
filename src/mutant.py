from dataclasses import dataclass
from git import Repo
from unidiff import PatchSet


@dataclass
class Mutant:
    mutant_id: int = -1
    modified_file_path: str = ""
    line_number_changed: int = -1
    previous_line: str = ""
    current_line: str = ""

    @classmethod
    def from_repo(cls, repo: Repo, mutant_id: int = None):
        current_diff = repo.index.diff(None)
        diff = repo.git.diff(repo.head, None)
        patchset = PatchSet(diff)

        modified_file_path = patchset[0].target_file[2:]  # Remove "b/" from the path
        changed_sourcecode_line = patchset[0][0].source_start
        previous_line = ''
        for line in patchset[0][0]:
            if line.is_added:
                current_line = str(line)[2:]
            if line.is_removed:
                current_line = str(line)[2:]

        return Mutant(mutant_id=mutant_id, modified_file_path=modified_file_path,
                      line_number_changed=changed_sourcecode_line,
                      previous_line=previous_line,
                      current_line=current_line)
