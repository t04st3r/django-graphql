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


class PublicHolidayMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        local_name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    public_holiday = graphene.Field(PublicHolidayType)

    @classmethod
    def mutate(cls, root, info, local_name, id):
        public_holiday = PublicHoliday.objects.get(pk=id)
        public_holiday.local_name = local_name
        public_holiday.save()
        # Notice we return an instance of this mutation
        return PublicHolidayMutation(public_holiday=public_holiday)


class Mutation(graphene.ObjectType):
    update_public_holiday = PublicHolidayMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
