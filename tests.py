import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_choice_with_empty_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_add_choice_with_long_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a', False)
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_and_select_correct_choices():
    question = Question(title='q1')
    a = question.add_choice('a', False)
    b = question.add_choice('b', False)
    question.set_correct_choices([b.id])
    result = question.select_choices([b.id])
    assert result == [b.id]

def test_select_incorrect_choice_returns_empty():
    question = Question(title='q1')
    a = question.add_choice('a', False)
    b = question.add_choice('b', False)
    result = question.select_choices([a.id])
    assert result == []

def test_select_more_than_max_selections_raises():
    question = Question(title='q1', max_selections=1)
    a = question.add_choice('a', True)
    b = question.add_choice('b', True)
    with pytest.raises(Exception):
        question.select_choices([a.id, b.id])

def test_choice_ids_are_incremental():
    question = Question(title='q1')
    a = question.add_choice('a')
    b = question.add_choice('b')
    assert b.id == a.id + 1

def test_select_multiple_correct_choices():
    question = Question(title='q1', max_selections=2)
    a = question.add_choice('a', False)
    b = question.add_choice('b', False)
    c = question.add_choice('c', False)
    question.set_correct_choices([b.id, c.id])
    result = question.select_choices([b.id, c.id])
    assert sorted(result) == sorted([b.id, c.id])

@pytest.fixture
def question_with_choices():
    question = Question(title='Sample', max_selections=2)
    a = question.add_choice('a', False)
    b = question.add_choice('b', True)
    c = question.add_choice('c', True)
    return question

def test_fixture_selects_correct_choices(question_with_choices):
    correct_ids = [choice.id for choice in question_with_choices.choices if choice.is_correct]
    question_with_choices.set_correct_choices(correct_ids)
    selected = question_with_choices.select_choices(correct_ids)
    assert sorted(selected) == sorted(correct_ids)

def test_fixture_remove_choice(question_with_choices):
    initial_len = len(question_with_choices.choices)
    choice_to_remove = question_with_choices.choices[0]
    question_with_choices.remove_choice_by_id(choice_to_remove.id)
    assert len(question_with_choices.choices) == initial_len - 1
