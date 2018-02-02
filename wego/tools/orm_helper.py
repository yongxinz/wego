# coding=utf-8
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models.aggregates import Func


class YMArrayAgg(ArrayAgg):
    '''
        SELECT ARRAY_AGG(DISTINCT "intset_productin"."grade") AS "items" FROM "intset_productin"

        print 111, ProductIn.objects.aggregate(
            width=YMArrayAgg('width', distinct=True),
            length=YMArrayAgg('length', distinct=True)
        )
    '''
    template = '%(function)s(%(distinct)s%(field)s)'

    def __init__(self, col, distinct=False, **extra):
        super(YMArrayAgg, self).__init__(col, distinct=(distinct and 'DISTINCT ' or ''), **extra)


class YMArrayElements(Func):
    '''
    SELECT
      DISTINCT jsonb_array_elements("intset_productin"."standard") -> 'num' AS numsd
    FROM "intset_productin";

    print ProductIn.objects.all().annotate(
            items=YMArrayElements('standard', 'num')
    ).values_list('items', flat=True)

    '''

    function = 'jsonb_array_elements'
    template = "DISTINCT %(function)s(%(expressions)s) -> '%(path)s'"
    arity = 1

    def __init__(self, expression, path, **extra):
        super(YMArrayElements, self).__init__(expression, path=path, **extra)
