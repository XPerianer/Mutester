import shutil
import zipfile

import pytest
from git import Repo

from mutester.mutant import Mutant
from mutester.semantic_mutant_analysis import SemanticMutantAnalysis


@pytest.fixture()
def mutant_fixture():
    with zipfile.ZipFile("tests/data/example_repo.zip", "r") as zip_ref:
        zip_ref.extractall("tests/data/")
    yield Mutant.from_repo(Repo("tests/data/example_repo"))
    shutil.rmtree("tests/data/example_repo")


def test_location_to_def(mutant_fixture):
    semantic_analysis = SemanticMutantAnalysis(mutant_fixture)

    method_names = []
    for i in range(1, 31):
        method_names.append(semantic_analysis.query_line_number(i))
    expected = ['A', 'A', 'A', 'A', 'A', '__init__', '__init__', '__init__', '__init__', '__init__', '__init__', 'A',
                'square', 'square', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'another_function', 'yet_another_help_function',
                'yet_another_help_function', 'another_function', 'another_function', None, None, None, None]
    assert (method_names == expected)


def test_changed_line_number(mutant_fixture):
    semantic_analysis = SemanticMutantAnalysis(mutant_fixture)
    assert (semantic_analysis.changed_line_number == 24)


def test_semantic_analysis(mutant_fixture):
    semantic_analysis = SemanticMutantAnalysis(mutant_fixture)
    assert (semantic_analysis.method_name() == "yet_another_help_function")


def test_parents_of_mutant_node(mutant_fixture):
    semantic_analysis = SemanticMutantAnalysis(mutant_fixture)
    assert (semantic_analysis.parent_names() == ['yet_another_help_function', 'another_function', 'A'])
