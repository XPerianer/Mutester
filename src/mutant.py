from dataclasses import dataclass


@dataclass
class Mutant:
    mutant_id: int = -1
    modified_file_path: str = ""
    line_number_changed: int = -1
    previous_line: str = ""
    current_line: str = ""
