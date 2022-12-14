import jsonschema

schema = {
    "type": "object",
    "properties": {
        "type": {
                    "enum" : ["Polygon", "MultiPolygon", "LineString", "Point", "MultiPoint", "MultiLineString", "GeometryCollection"]
                },
        "coodinates": { "type": "array"}
    },
    "required": ["type", "coordinates"]
}


def json_schema_checker(request:dict) -> dict:
    """Esta função realiza a validação do json de entrada com o schema definido, se houver erros, retorna um json com os erros. Se não houver erros, retorna None.
    O schema foi definido de acordo com as normas do GeoJSON e aceitam todas as geometrias oficialmente suportadas.

    Args:
        request (dict): este argumento é um dicionário que representa o json de entrada. Nele deve ser definido o campo "type" e o campo "coordinates".

    Returns:
        dict: retorna um dicionário com os erros encontrados. Se não houver erros, retorna None.

    Exemplos:
        >>> json_schema_checker({'type': 'Polygon', 'coordinates': [[[1, 2], [3, 4], [5, 6], [1, 2]]]})
        None

        >>> json_schema_checker({'type': 'Polygon', 'coordinotes': [[[1, 2], [3, 4], [5, 6], [1, 2]]]})
        errorMessage = {
            "type": https://dominio.visiona/example-error,
            "title": 'coordinates' é um campo obrigatório',
            "status": 400,
            "detail": A requisição não possui os campos obrigatórios para processamento ou valores estão fora do formato especificado,
        }
    """
    v = jsonschema.Draft7Validator(schema, format_checker=jsonschema.draft7_format_checker)

    errorMessage = {
        "type": None,
        "title": None,
        "status": None,
        "detail": None,
    }
    
    try:
        v.validate(request)
        return None
    except (jsonschema.exceptions.ValidationError):
        errorMessage['campos'] = []
        for error in sorted(v.iter_errors(request), key=str):
            string = str(error.message)
            string = string.replace("is a required property", "é um campo obrigatório")
            string = string.replace("is not of type", "não é do tipo")
            string = string.replace("is not one of", "não é de nenhum dos tipos ")
            errorMessage['campos'].append(string)

        errorMessage['type'] = "https://vpedrota.github.io/valida_geometrias/core_functions.html"
        errorMessage['status'] = 400
        errorMessage['detail'] = "A requisição não possui os campos obrigatórios para processamento ou valores estão fora do formato especificado"
        errorMessage['title'] = "A requisição não pode ser processada devido a validação de campos"
        return errorMessage