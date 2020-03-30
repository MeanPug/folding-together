import json


def cast_numbers(event, context):
    """ takes numeric values from a dynamodb result and converts them to numbers for future processing """
    conversion_requested = event.get("ConvertIn")
    converted = {}

    print(f'got request to convert {conversion_requested}')

    for k, v in conversion_requested.items():
        try:
            converted[k] = int(v)
        except TypeError:
            print(f'failed to convert {k}')

    return converted
