from __future__ import unicode_literals

from graphql.language.ast import (BooleanValue, FloatValue, IntValue,
                                  StringValue, ListValue, ObjectValue)

from graphene.types.scalars import MIN_INT, MAX_INT
from .scalars import Scalar


class JSON(Scalar):
    """
    The `JSON` scalar type represents JSON values as specified by
    [ECMA-404](http://www.ecma-international.org/
    publications/files/ECMA-ST/ECMA-404.pdf).
    """

    @staticmethod
    def identity(value):
        return value

    serialize = identity
    parse_value = identity

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (StringValue, BooleanValue)):
            return ast.value
        elif isinstance(ast, IntValue):
            num = int(ast.value)
            if MIN_INT <= num <= MAX_INT:
                return num
        elif isinstance(ast, FloatValue):
            return float(ast.value)
        elif isinstance(ast, ListValue):
            return [JSON.parse_literal(value) for value in ast.values]
        elif isinstance(ast, ObjectValue):
            return {field.name.value: JSON.parse_literal(field.value) for field in ast.fields}
        else:
            return None
