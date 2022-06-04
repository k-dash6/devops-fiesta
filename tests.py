import pytest
from pytest_mock import MockerFixture

from apps import Cocktails


@pytest.fixture(scope='session')
def cocktails_obj():
    return Cocktails()


def test_read__correct_data(mocker: MockerFixture):
    test_file = """ Коктейль Пиранья
3
Водка – 37 мл (6 ч. л.)
ликер, коричневый – 25 мл (1,5 ст. л.)
Кола, сильно охлажденная – 25 мл (1,5 ст. л.)
Влейте спиртное в низкий стакан, заполненный большим количеством колотого льда. Хорошо размешайте. Затем добавьте колу.
Коктейль Оазис
3
Джин – 50 мл (3 ст. л.)
Ликер «Кюрасао» голубой – 12 мл (2 ч. л.)
Тоник – 100 мл
Влейте джин в стакан, наполовину заполненный колотым льдом. Добавьте Кюрасао, влейте тоник и перемешайте. 
Украсьте долькой лимона и веточкой мяты.
"""

    mocker.patch('builtins.open', mocker.mock_open(read_data=test_file))
    c = Cocktails()
    assert len(c.cocktails) == 2
    assert all([isinstance(r, Cocktails.Cocktail) for r in c.cocktails])


def test_read__empty_data(mocker: MockerFixture):
    test_file = """"""

    mocker.patch('builtins.open', mocker.mock_open(read_data=test_file))
    c = Cocktails()
    assert not c.cocktails


def test_get_receipts__empty_list(cocktails_obj):
    result = cocktails_obj.get_receipts([])
    assert not result


def test_get_receipts__list_with_one_ingredient(cocktails_obj):
    result = cocktails_obj.get_receipts(['виски'])
    assert not result


def test_get_receipts__list_with_multiple_ingredients(cocktails_obj):
    result = cocktails_obj.get_receipts(['ананасовый', 'ром', 'сливки'])
    assert len(result) == 2
    assert all([isinstance(r[0], Cocktails.Cocktail) for r in result])
    assert result[0][0].name == 'Коктейль Пина колада'
    assert result[0][0].receipt == 'В блендер сложить лед, налить ананасовый сок, ром, ' \
                                   'сливки (или кокосовое молоко) и пульсировать до однородного состояния. ' \
                                   'Налить коктейль в порционные бокалы и украсить дольками ананаса.'
    assert result[0][0].ingredients == {'ананасовый', 'ром', 'сливки'}
    assert result[0][0].components == ['Ананасовый сок, охлажденный - 3/4 стакана', 'ром - 1/2 стакана', 'Сливки или кокосовое молоко - 1/2 стакана']


def test_get_receipts__list_with_another_multiple_ingredient(cocktails_obj):
    result = cocktails_obj.get_receipts(['джин', 'вермут', 'ликер'])
    assert len(result) == 3
    assert all([isinstance(r[0], Cocktails.Cocktail) for r in result])
    assert result[0][0].name == 'Коктейль Оазис'
    assert result[0][0].receipt == 'Влейте джин в стакан, наполовину заполненный колотым льдом. Добавьте Кюрасао, влейте тоник и перемешайте. Украсьте долькой лимона и веточкой мяты.'
    assert result[0][0].ingredients == {'ликер', 'джин', 'тоник'}
    assert result[0][0].components == ['Джин – 50 мл (3 ст. л.)', 'Ликер «Кюрасао» голубой – 12 мл (2 ч. л.)', 'Тоник – 100 мл']


def test_get_receipts__list_with_incorrect_ingredient(cocktails_obj):
    result = cocktails_obj.get_receipts(['пиво', 'сидр'])
    assert not result


def test_get_receipts__list_with_correct_and_incorrect_ingredient(cocktails_obj):
    result = cocktails_obj.get_receipts(['водка', 'тест'])
    assert not result


def test_get_receipts__list_with_incorrect_ingredient_type(cocktails_obj):
    result = cocktails_obj.get_receipts([1, 2])
    assert not result


def test_get_receipts__str_instead_of_list(cocktails_obj):
    result = cocktails_obj.get_receipts('тест')
    assert not result


def test_get_random(cocktails_obj):
    result = cocktails_obj.get_random_receipt()
    assert isinstance(result, Cocktails.Cocktail)
