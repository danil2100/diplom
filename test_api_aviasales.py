import pytest
import requests

BASE_URL = "https://ariadne.aviasales.com/api/gql"


def test_valid_direction_page_blocks():
    payload = {
        "query": "query DirectionPageBlocksQuery($brand: Brand!, $input: DirectionPageBlocksV2Input!) { direction_page_blocks_v2(input: $input, brand: $brand) { blocks { __typename } } }",
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


def test_search_by_valid_date():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { depart_date value currency } places { cities { city { iata } } } } }",
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


def test_search_nonexistent_city():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
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


def test_past_date_search():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { value } cheapest_direct { value } places { cities { city { iata } } } } }",
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


def test_empty_search_fields():
    payload = {
        "query": "query GetBestPricesV2($input: BestPricesV2Input!, $brand: Brand!) { best_prices_v2(input: $input, brand: $brand) { cheapest { value } } }",
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