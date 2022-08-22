core\_functions.py
======================

O schema foi definido de acordo com as normas do GeoJSON e aceitam todas as geometrias oficialmente suportadas. Consulte a seguir o schema definido::

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

   Nesta parte apenas a verificação do formato é feita, o conteúdo não é verificado. A verificação do conteúdo é feita posteriormente utilizando o Postgis.
.. automodule:: core_functions
   :members:
   :undoc-members:
   :show-inheritance:
