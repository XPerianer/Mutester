import re
from dataclasses import dataclass


def textToBool(t: str):
    if t in ["failed", "skipped", "error", "xfailed"]:  # If not executed, we tread it as false
        return False
    elif t == "passed":
        return True
    else:
        raise Exception(
            "Value of outcome could not be interpreted as true or false. t was: {}".format(
                t
            )
        )


@dataclass
class Execution:
    outcome: bool = None
    test_id: int = None
    full_name: str = None
    name: str = None
    filepath: str = None
    duration: float = None
    mutant_id: int = None

    setup_outcome: bool = None
    setup_duration: float = None

    call_outcome: bool = None
    call_duration: float = None

    teardown_outcome: bool = None
    teardown_duration: float = None

    contains_branch: bool = None
    contains_loop: bool = None
    contains_math_operands: bool = None
    contains_equality_comparison: bool = None

    @classmethod
    def fromJson(self, json, mutant_id=None, repository_path=None):
        t = Execution()
        t.mutant_id = mutant_id
        t.outcome = textToBool(json["outcome"])
        t.test_id = json["run_index"]
        t.full_name = json["name"]
        [t.filepath, t.name] = t.full_name.split("::", 1)
        t.duration = json["duration"]

        t.setup_outcome = textToBool(json["setup"]["outcome"])
        t.setup_duration = json["setup"]["duration"]

        if t.setup_outcome:
            t.call_outcome = textToBool(json["call"]["outcome"])
            t.call_duration = json["call"]["duration"]
            if t.call_outcome:
                t.teardown_outcome = textToBool(json["teardown"]["outcome"])
                t.teardown_duration = json["teardown"]["duration"]

        try:
            # TODO: Should be something like os.join
            with open(repository_path + '/' + t.filepath, "r") as file:
                t.context_analysis(file.read())
        except:  # noqa: E722
            # TODO: Find out what the right expection here is
            print("Failed to open the test file for regex analysis or analysing the test")
            pass
        return t

    def context_analysis(self, string: str):
        # Find position of test in file:
        # pattern = "def " + self.name + r'\[\s\S\]*?def'
        pattern = 'def ' + re.escape(self.name) + r'[\s\S]*?def'
        match = re.search(pattern, string)
        if match:
            context = match.group(0)
            self.contains_branch = re.search("if|else|switch", context) is not None
            self.contains_loop = re.search("for|while", context) is not None
            self.contains_math_operands = re.search("[-+*/]", context) is not None
            self.contains_equality_comparison = re.search("==", context) is not None
