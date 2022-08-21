import psycopg2
import jsonschema
import json
from flask import Flask, request

def create_app():

    app = Flask(__name__)

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

    def get_db_connection():
        conn = psycopg2.connect(
            database="db_name",
            user="user",
            password="pass",
            host="0.0.0.0"
        )

        return conn

    def json_schema(request):
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


    @app.route("/", methods=['POST'])
    def index():

        json_data = request.json
        format_errors = json_schema(json_data)

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
            print(data[0])
        except psycopg2.errors.InternalError_ as e:
            
            errorMessage = {
                "type": None,
                "title": None,
                "status": None,
                "detail": None,
            }   

            errorMessage['type'] = "https://dominio.visiona/example-error"
            errorMessage['status'] = 400
            errorMessage['title'] = "A requisição não pode ser processada devido a erros de geometria, geometria inválida!"
            errorMessage['detail'] = str(e).split('HINT')[0]
            return errorMessage, 400

        cur.close()
        conn.close()
        return json.dumps(json_data)
    return app

app = create_app()


