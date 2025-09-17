import requests
import allure


BASE_URL = "https://ariadne.aviasales.com/api/gql"


@allure.title("Проверка получения блоков направления: Ижевск → Москва")
@allure.description(
    "Тест проверяет корректность ответа сервера при запросе данных о блоках "
    "для направления 'Ижевск (IJK)' → 'Москва (MOW)'. Ожидается возврат "
    "структурированных данных с блоками типа 'HowToGetDirectFlights' и другими "
    "компонентами интерфейса. Проверяется статус 200 и наличие данных."
)
@allure.severity('critical')
def test_valid_direction_page_blocks():
    payload = {
        "query": "query DirectionPageBlocksQuery($brand: Brand!, $input: DirectionPageBlocksV2Input!) { "
                 "direction_page_blocks_v2(input: $input, brand: $brand) { "
                 "blocks { __typename } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "market": "ru",
                "language": "ru",
                "origin": {"iata": "IJK", "place_type": "CITY"},
                "destination": {"flightable_place": {"iata": "MOW", "place_type": "CITY"}},
                "currency": "rub",
                "passport_country": "RU",
                "auid": "SkxOR2ZrwSozc2VyNFBSAg==",
                "application": "selene",
                "trip_class": "Y"
            }
        },
        "operation_name": "direction_page_blocks_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("data") is not None
    assert len(data["data"]["direction_page_blocks_v2"]["blocks"]) > 0


@allure.title("Поиск билетов по конкретной дате вылета: 21.10.2025")
@allure.description(
    "Тест проверяет возможность получения cheapest-билетов при указании "
    "валидной даты вылета (2025-10-21) между городами IJK и MOW. "
    "Проверяется корректность возвращаемых полей: depart_date, value, currency, "
    "а также наличие информации о городах и аэропортах."
)
@allure.severity('critical')
def test_search_by_valid_date():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { "
                 "best_prices_v2(input: $input, brand: $brand) { "
                 "cheapest { depart_date value currency } "
                 "places { cities { city { iata } } } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": ["2025-10-21"]},
                "origin": "IJK",
                "destination": "MOW",
                "one_way": True,
                "market": "ru",
                "filters": {}
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["best_prices_v2"]["cheapest"]["depart_date"] == "2025-10-21"
    assert data["data"]["best_prices_v2"]["cheapest"]["value"] > 0


@allure.title("Поиск с несуществующим кодом города назначения (15786238)")
@allure.description(
    "Тест проверяет реакцию системы на некорректный IATA-код города назначения ('15786238'). "
    "Ожидается, что сервер вернёт ошибку 'city can not be resolved' в поле errors, "
    "а данные (data) будут null, что соответствует бизнес-логике обработки неверных входных данных."
)
@allure.severity('critical')
def test_search_nonexistent_city():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { "
                 "best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": ["2025-10-21"]},
                "origin": "IJK",
                "destination": "15786238",
                "one_way": True,
                "market": "ru",
                "filters": {}
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "errors" in data
    assert "city can not be resolved" in data["errors"][0]["message"]
    assert data["data"] is None


@allure.title("Поиск билетов с датой вылета из прошлого (2024-06-10)")
@allure.description(
    "Тест проверяет поведение системы при запросе даты вылета, которая уже прошла (2024-06-10). "
    "Ожидается, что cheapest-предложения будут null, но информация о городах (places) должна быть возвращена, "
    "что позволяет системе отображать информацию даже для прошедших дат."
)
@allure.severity('high')
def test_past_date_search():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { "
                 "best_prices_v2(input: $input, brand: $brand) { "
                 "cheapest { value } cheapest_direct { value } "
                 "places { cities { city { iata } } } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": ["2024-06-10"]},
                "origin": "IJK",
                "destination": "MOW",
                "one_way": True,
                "market": "ru",
                "filters": {}
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["best_prices_v2"]["cheapest"] is None
    assert data["data"]["best_prices_v2"]["cheapest_direct"] is None
    assert len(data["data"]["best_prices_v2"]["places"]["cities"]) > 0


@allure.title("Поиск с пустыми полями: отсутствие города отправления и назначения")
@allure.description(
    "Тест проверяет обработку ситуации, когда пользователь не выбрал ни город отправления, ни город назначения. "
    "Ожидается, что сервер вернёт ошибку 'city can not be resolved', а данные будут null, "
    "что предотвращает некорректный поиск без обязательных параметров."
)
@allure.severity('critical')
def test_empty_search_fields():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { "
                 "best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": []},
                "origin": "",
                "destination": "",
                "one_way": False,
                "market": "ru",
                "filters": {}
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "errors" in data
    assert "city can not be resolved" in data["errors"][0]["message"]
    assert data["data"] is None


@allure.title("Поиск с недопустимым параметром booking_classes: ['Y','C','F']")
@allure.description(
    "Тест проверяет, что система корректно отклоняет запрос с несуществующим фильтром 'booking_classes'. "
    "Ожидается HTTP-статус 422 Unprocessable Entity и сообщение об ошибке 'unknown field' в пути filters.booking_classes. "
    "Это подтверждает, что API строго валидирует входные параметры и не принимает неизвестные поля."
)
@allure.severity('high')
def test_booking_classes_invalid():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": ["2025-06-21"]},
                "origin": "KHV",
                "destination": "MOW",
                "one_way": True,
                "market": "ru",
                "filters": {
                    "no_visa_at_transfer": False,
                    "with_baggage": False,
                    "direct": False,
                    "booking_classes": ["Y", "C", "F"]
                }
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "errors" in data
    assert data["errors"][0]["message"] == "unknown field"
    assert data["errors"][0]["path"] == ["variable", "input", "filters", "booking_classes"]
    assert data["data"] is None


@allure.title("Поиск с количеством пассажиров более 10 (adults=11)")
@allure.description(
    "Тест проверяет ограничение системы по максимальному количеству взрослых пассажиров. "
    "Указание adults=11 должно вызвать ошибку валидации 'unknown field' в пути filters.adults. "
    "Это подтверждает, что API защищён от передачи неограниченных значений и реализует логические ограничения."
)
@allure.severity('high')
def test_adults_over_limit():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
        "variables": {
            "brand": "AS",
            "input": {
                "currency": "rub",
                "dates": {"depart_dates": ["2025-06-21"]},
                "origin": "KHV",
                "destination": "MOW",
                "one_way": True,
                "market": "ru",
                "filters": {
                    "no_visa_at_transfer": False,
                    "with_baggage": False,
                    "direct": False,
                    "adults": 11
                }
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "errors" in data
    assert data["errors"][0]["message"] == "unknown field"
    assert data["errors"][0]["path"] == ["variable", "input", "filters", "adults"]
    assert data["data"] is None