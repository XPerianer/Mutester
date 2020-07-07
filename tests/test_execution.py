import json

from mutester.execution import Execution


def test_parsing():
    json_test = json.loads(
        '{"name": "tests/test_appctx.py::test_basic_url_generation", "duration": 1, "run_index": 0, "setup": {"name": "setup", "duration": 2, "outcome": "passed"}, ' \
        '"call": {"name": "call", "duration": 3, "outcome": "passed"}, "teardown": {"name": "teardown", "duration": 4, "outcome": "passed"}, "outcome": "passed"}'
    )
    execution_reference = Execution(
        full_name="tests/test_appctx.py::test_basic_url_generation",
        duration=1,
        test_id=0,
        setup_duration=2,
        setup_outcome=True,
        call_duration=3,
        call_outcome=True,
        teardown_duration=4,
        teardown_outcome=True,
        outcome=True,
        name="test_basic_url_generation",
        filepath="tests/test_appctx.py",
    )
    assert Execution.fromJson(json_test) == execution_reference

def test_regex_parsing():
    execution = Execution()
    execution.name = "test_url_generation_without_context_fails"
    execution.context_analysis("""
def test_url_generation_requires_server_name(app):
    with app.app_context():
        with pytest.raises(RuntimeError):
            flask.url_for("index")


def test_url_generation_without_context_fails():
    while(True):
        if True:

    with pytest.raises(RuntimeError):
        flask.url_for("index")


def test_request_context_means_app_context(app):
    with app.test_request_context():
        assert flask.current_app._get_current_object() == app
    assert flask._app_ctx_stack.top is None
                               "")
""")
    assert(not execution.contains_equality_comparison)
    assert(not execution.contains_math_operands)
    assert(execution.contains_loop)
    assert(execution.contains_branch)


