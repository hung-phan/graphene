from ..jsontype import JSON
from ..objecttype import ObjectType
from ..schema import Schema


class Query(ObjectType):
    json = JSON(input=JSON())

    def resolve_json(self, args, context, info):
        input = args.get('input')
        return input


schema = Schema(query=Query)


def test_json_query_variable():
    for json_value in [
        1,
        1.1,
        True,
        'str',
        [1, 2, 3],
        [1.1, 2.2, 3.3],
        [True, False],
        ['str1', 'str2'],
        {
            'key_a': 'a',
            'key_b': 'b'
        },
        {
            'int': 1,
            'float': 1.1,
            'boolean': True,
            'string': 'str',
            'int_list': [1, 2, 3],
            'float_list': [1.1, 2.2, 3.3],
            'boolean_list': [True, False],
            'string_list': ['str1', 'str2'],
            'nested_dict': {
                'key_a': 'a',
                'key_b': 'b'
            }
        },
        None
    ]:
        result = schema.execute(
            '''query Test($json: JSON){ json(input: $json) }''',
            variable_values={'json': json_value}
        )
        assert not result.errors
        assert result.data == {
            'json': json_value
        }


def test_json_parse_literal_query():
    result = schema.execute(
        '''
        query {
            json(input: {
                int: 1,
                float: 1.1
                boolean: true,
                string: "str",
                int_list: [1, 2, 3],
                float_list: [1.1, 2.2, 3.3],
                boolean_list: [true, false]
                string_list: ["str1", "str2"],
                nested_dict: {
                    key_a: "a",
                    key_b: "b"
                },
                empty_key: undefined
            })
        }
        '''
    )
    assert not result.errors
    assert result.data == {
        'json': {
            'int': 1,
            'float': 1.1,
            'boolean': True,
            'string': 'str',
            'int_list': [1, 2, 3],
            'float_list': [1.1, 2.2, 3.3],
            'boolean_list': [True, False],
            'string_list': ['str1', 'str2'],
            'nested_dict': {
                'key_a': 'a',
                'key_b': 'b'
            },
            'empty_key': None
        }
    }
