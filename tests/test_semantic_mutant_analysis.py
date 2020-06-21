from src.semantic_mutant_analysis import SemanticMutantAnalysis


def test_location_to_def():
    semantic_analysis = SemanticMutantAnalysis("data")

    method_names = []
    for i in range(1, 31):
        method_names.append(semantic_analysis.query_line_number(i))
    expected = ['A', 'A', 'A', 'A', 'A', '__init__', '__init__', '__init__', '__init__', '__init__', '__init__', 'A', 'square', 'square', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'another_function', 'yet_another_help_function', 'yet_another_help_function', 'another_function', 'another_function', None, None, None, None]
    assert(method_names == expected)
