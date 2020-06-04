from dataclasses import dataclass


def textToBool(t: str):
    if t == "failed" or t == "skipped" or t == "error":  # If not executed, we tread it as false
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

    @classmethod
    def fromJson(self, json, mutant_id):
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
        return t
