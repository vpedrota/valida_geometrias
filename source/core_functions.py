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


def json_schema(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
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

        errorMessage['type'] = "https://dominio.visiona/example-error"
        errorMessage['status'] = 400
        errorMessage['detail'] = "A requisição não possui os campos obrigatórios para processamento ou valores estão fora do formato especificado"
        errorMessage['title'] = "A requisição não pode ser processada devido a validação de campos"
        return errorMessage