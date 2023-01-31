import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


#параметризация входных данных (создание фикстур)
#например, когда хотим протестировать разные параметры фильтров или граничные условия

@pytest.fixture
def client():
    """Фикстура для клиента API"""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов"""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов"""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

#проверка получения 1-ого курса (retrieve-логика)

@pytest.mark.django_db
def test_1_retrieve(client, course_factory):
    # Arrange - создаем курс через фабрику
    test_course = course_factory(_quantity=1)
    # Act - строим урл и делаем запрос через тестовый клиент
    response = client.get(f'/api/v1/courses/{test_course[0].id}/')
    data = response.json()
    # Assert - проверяем, что вернулся именно тот курс, который запрашивали
    assert response.status_code == 200
    assert data['id'] == test_course[0].id
    assert data['name'] == test_course[0].name

#проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_list(client, course_factory):
    # Arrange - вызываем фабрики
    test_course = course_factory(_quantity=10)
    # Act - делаем запрос
    response = client.get('/api/v1/courses/')
    data = response.json()
    # Assert - проверяем
    assert response.status_code == 200
    for iteration, courses in enumerate(data):
        assert courses['id'] == test_course[iteration].id

#проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id(client, course_factory):
    # Arrange - создаем курсы через фабрику
    test_course = course_factory(_quantity=100)
    # Assert - проверяем результат запроса с фильтром
    response = client.get('/api/v1/courses/', {'id': test_course[10].id})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == test_course[10].id
    assert data[0]['name'] == test_course[10].name

#проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name(client, course_factory):
    test_course = course_factory(_quantity=100)
    response = client.get('/api/v1/courses/', {'name': test_course[10].name})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == test_course[10].name

#тест успешного создания курса
@pytest.mark.django_db
def test_create(client, course_factory):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'Стать специалистом по машинному обучению'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

#тест успешного обновления курса
@pytest.mark.django_db
def test_update(client, course_factory):
    test_course = course_factory(_quantity=1)
    update = {'name': 'new name'}
    response = client.patch(f'/api/v1/courses/{test_course[0].id}/', data=update)
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == update ['name']

#тест успешного удаления курса
@pytest.mark.django_db
def test_delete(client, course_factory):
    test_course = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{test_course[0].id}/')
    request = client.get(f'/api/v1/courses/{test_course[0].id}/')
    assert response.status_code == 204
    assert request.status_code == 404


