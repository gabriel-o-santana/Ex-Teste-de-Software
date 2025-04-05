import pytest
from model import Question


def test_create_question():
    question = Question(title="q1")
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title="q1")
    question2 = Question(title="q2")
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title="")
    with pytest.raises(Exception):
        Question(title="a" * 201)
    with pytest.raises(Exception):
        Question(title="a" * 500)


def test_create_question_with_valid_points():
    question = Question(title="q1", points=1)
    assert question.points == 1
    question = Question(title="q1", points=100)
    assert question.points == 100


def test_create_choice():
    question = Question(title="q1")

    question.add_choice("a", False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == "a"
    assert not choice.is_correct


def test_add_multiple_choices():
    question = Question(title="q1")
    question.add_choice("a", False)
    question.add_choice("b", True)

    assert len(question.choices) == 2
    assert question.choices[0].text == "a"
    assert question.choices[1].text == "b"


def test_remove_choice_by_id():
    question = Question(title="q1")
    choice_a = question.add_choice("a", False)
    choice_b = question.add_choice("b", True)

    question.remove_choice_by_id(choice_a.id)

    assert len(question.choices) == 1
    assert question.choices[0].text == "b"


def test_remove_all_choices():
    question = Question(title="q1")
    question.add_choice("a", False)
    question.add_choice("b", True)

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_select_correct_choices():
    question = Question(title="q1")
    choice_a = question.add_choice("a", False)
    choice_b = question.add_choice("b", True)
    question.set_correct_choices([choice_b.id])

    selected_choices = question.select_choices([choice_b.id])

    assert selected_choices == [choice_b.id]


def test_select_more_than_max_selections():
    question = Question(title="q1", max_selections=1)
    question.add_choice("a", False)
    question.add_choice("b", True)

    with pytest.raises(Exception):
        question.select_choices([choice.id for choice in question.choices])


def test_set_correct_choices():
    question = Question(title="q1")
    choice_a = question.add_choice("a", False)

    question.set_correct_choices([choice_a.id])

    assert choice_a.is_correct == True


def test_create_question_with_points_out_of_range():

    with pytest.raises(Exception):
        Question(title="q1", points=0)
    with pytest.raises(Exception):
        Question(title="q1", points=101)


def test_create_choice_with_invalid_text():
    question = Question(title="q1")

    with pytest.raises(Exception):
        question.add_choice("", False)

    with pytest.raises(Exception):
        question.add_choice("a" * 101, False)


def test_validate_invalid_choice_id():
    question = Question(title="q1")
    choice_a = question.add_choice("a", False)

    with pytest.raises(Exception):
        question._choice_by_id("invalid_id")


def test_max_selections_greater_than_one():
    question = Question(title='q1', max_selections=3)
    choice_a = question.add_choice('a', False)
    choice_b = question.add_choice('b', True)
    choice_c = question.add_choice('c', False)

    question.set_correct_choices([choice_a.id, choice_b.id, choice_c.id])
    selected_choices = question.select_choices([choice_a.id, choice_b.id, choice_c.id])
    
    assert selected_choices == [choice_a.id, choice_b.id, choice_c.id]
