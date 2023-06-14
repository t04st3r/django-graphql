import graphene
from graphene_django import DjangoObjectType

from .models import PublicHoliday


class PublicHolidayType(DjangoObjectType):
    class Meta:
        model = PublicHoliday
        fields = "__all__"


class Query(graphene.ObjectType):
    all_holidays = graphene.List(PublicHolidayType)
    holiday_by_country = graphene.List(
        PublicHolidayType, country=graphene.String(required=True)
    )

    def resolve_all_holidays(root, info):
        return PublicHoliday.objects.all()

    def resolve_holiday_by_country(root, info, country):
        return PublicHoliday.objects.filter(country=country)


schema = graphene.Schema(query=Query)
