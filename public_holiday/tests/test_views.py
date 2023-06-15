import pytest

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from .factories import PublicHolidayFactory


@pytest.mark.django_db
class TestPublicHolidayAPI:
    def test_public_holiday_list_success(self):
        batch = PublicHolidayFactory.create_batch(10)
        client = APIClient()
        response = client.get("/public_holiday/")
        assert response.status_code == status.HTTP_200_OK
        batch_ids = [model.id for model in batch]
        response_dict = response.json()
        assert response_dict["count"] == 10
        for model in response_dict["results"]:
            assert model["id"] in batch_ids

    def test_public_holiday_detail_success(self):
        today = timezone.now().date()
        model = PublicHolidayFactory(
            name="Holy Moly", local_name="Santo Cielo!", date=today
        )
        client = APIClient()
        response = client.get(f"/public_holiday/{model.id}/")
        assert response.status_code == status.HTTP_200_OK
        response_dict = response.json()
        assert response_dict["id"] == model.id
        assert response_dict["date"] == str(model.date)
        assert response_dict["name"] == model.name
        assert response_dict["local_name"] == model.local_name
        assert response_dict["country"] == str(model.country)


@pytest.mark.django_db
class TestGraphQLAPI:
    def test_public_holiday_list_graphql_success(self):
        graphql_query = """
        query {
            allHolidays {
                id
                name
                localName
            }
        }
        """
        batch = PublicHolidayFactory.create_batch(10)
        client = APIClient()
        response = client.post("/graphql", {"query": graphql_query}, format="json")
        assert response.status_code == status.HTTP_200_OK
        batch_ids = [model.id for model in batch]
        response_dict = response.json()
        assert len(response_dict["data"]["allHolidays"]) == 10
        for model in response_dict["data"]["allHolidays"]:
            assert int(model["id"]) in batch_ids
            assert "country" not in model.keys()
            assert "date" not in model.keys()

    def test_public_holiday_by_country_graphql_success(self):
        graphql_query_uy = """
        query {
            holidayByCountry(country: "UY"){
                id
                localName
                name
                date
            }
        }
        """
        graphql_query_it = """
        query {
            holidayByCountry(country: "IT"){
                id
                localName
                name
                country
            }
        }
        """
        graphql_query_us = """
        query {
            holidayByCountry(country: "US"){
                id
                localName
                name
                country
            }
        }
        """
        it_batch = PublicHolidayFactory.create_batch(10, country="IT")
        us_batch = PublicHolidayFactory.create_batch(15, country="US")
        batch_ids_it = [model.id for model in it_batch]
        batch_ids_us = [model.id for model in us_batch]
        client = APIClient()
        response = client.post("/graphql", {"query": graphql_query_uy}, format="json")
        assert response.status_code == status.HTTP_200_OK
        response_dict = response.json()
        assert response_dict["data"]["holidayByCountry"] == []
        response = client.post("/graphql", {"query": graphql_query_it}, format="json")
        response_dict = response.json()
        assert len(response_dict["data"]["holidayByCountry"]) == 10
        for model in response_dict["data"]["holidayByCountry"]:
            assert int(model["id"]) in batch_ids_it
            assert model["country"] == "IT"
        response = client.post("/graphql", {"query": graphql_query_us}, format="json")
        response_dict = response.json()
        assert len(response_dict["data"]["holidayByCountry"]) == 15
        for model in response_dict["data"]["holidayByCountry"]:
            assert int(model["id"]) in batch_ids_us
            assert model["country"] == "US"

    def test_public_holiday_graphql_mutation_success(self):
        graphql_mutation = """
            mutation MyMutation {
                updatePublicHoliday(id: "1", localName: "Pizza") {
                    publicHoliday {
                        id
                        localName
                    }
                }
            }
        """
        public_holiday = PublicHolidayFactory(local_name="Hamburger", id=1)
        client = APIClient()
        response = client.post("/graphql", {"query": graphql_mutation}, format="json")
        assert response.status_code == status.HTTP_200_OK
        response_dict = response.json()
        response_model = response_dict["data"]["updatePublicHoliday"]["publicHoliday"]
        assert response_model["id"] == "1"
        assert response_model["localName"] == "Pizza"
        public_holiday.refresh_from_db()
        assert public_holiday.local_name == "Pizza"
