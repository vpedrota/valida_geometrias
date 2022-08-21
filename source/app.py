import psycopg2
import jsonschema
import json
from flask import Flask, request

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

def create_app():

    app = Flask(__name__)


    def get_db_connection():
        conn = psycopg2.connect(
            database="db_name",
            user="user",
            password="pass",
            host="0.0.0.0"
        )

        return conn



    @app.route("/", methods=['POST'])
    def index():

        json_data = request.json
        format_errors = json_schema(json_data)
        error_detail = None
        if(format_errors != None):
            return format_errors, 400

        conn = get_db_connection()
        cur = conn.cursor()
        sql = f"""
                SELECT ST_IsValidReason(ST_AsText(ST_GeomFromGeoJSON(' {json.dumps(request.json)} '))) As wkt;
            """
        try:

            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            conn.close()
            if(data[0][0] == 'Valid Geometry'):
                return 'Valid Geometry', 200

        except psycopg2.errors.InternalError_ as e:
            error_detail = str(e)

        errorMessage = {
            "type": None,
            "title": None,
            "status": None,
            "detail": None,
        }   

        if(error_detail == None):
            error_detail = data[0][0]

        errorMessage['type'] = "https://dominio.visiona/example-error"
        errorMessage['status'] = 400
        errorMessage['title'] = "A requisição não pode ser processada devido a erros de geometria, geometria inválida!"
        errorMessage['detail'] = error_detail.split('HINT')[0]
        cur.close()
        conn.close()
        return errorMessage, 400

    return app

app = create_app()


