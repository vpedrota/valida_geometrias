import psycopg2
import jsonschema
import json
from flask import Flask, request
from core_functions import *

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


