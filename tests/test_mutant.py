import shutil

import pytest

from mutester.semantic_mutant_analysis import SemanticMutantAnalysis
from mutester.mutant import Mutant
from git import Repo

import zipfile

@pytest.fixture()
def mutant_fixture():
    with zipfile.ZipFile("tests/data/example_repo.zip", "r") as zip_ref:
        zip_ref.extractall("tests/data/")
    yield Mutant.from_repo(Repo("tests/data/example_repo"))
    shutil.rmtree("tests/data/example_repo")

def test_regex_analysis(mutant_fixture):
    mutant_fixture.context_analysis("if (test + 1 == 3)")
    assert(mutant_fixture.contains_branch)
    assert(mutant_fixture.contains_math_operands)
    assert(not mutant_fixture.contains_loop)
    assert(mutant_fixture.contains_equality_comparison)
    mutant_fixture.context_analysis("while(True): do nothing")
    assert(not mutant_fixture.contains_branch)
    assert(not mutant_fixture.contains_math_operands)
    assert(mutant_fixture.contains_loop)
    assert(not mutant_fixture.contains_equality_comparison)