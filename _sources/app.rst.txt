app.py
==========

      Neste módulo temos as principais funções para o funcionamento do sistema. Aqui temos a definição dos endpoints da API e também o envio do GeoJSON
      após a sua verificação de seu formato, para que seja verificado sua integridade. Consulte a definição do endpoint a seguir::

            @app.route("/", methods=['POST'])
            def index():

                  json_data = request.json
                  format_errors = json_schema_checker(json_data)
                  error_detail = None
                  if(format_errors != None):
                        return format_errors, 400

                  conn = get_db_connection()
                  cur = conn.cursor()
                  sql = f"""
                        SELECT ST_IsValidReason(ST_AsText(ST_GeomFromGeoJSON(' {json.dumps(request.json)} ')));
                        """
                  try:
                        ...
      
      Na função acima, temos um GeoJSON deve ser enviado via POST para o endpoint /, e o sistema verifica se o GeoJSON é válido. Primeiro ele realiza a verificação
      do formato e de seus repectivos campos, em seguida, verifica a integridade do GeoJSON. Caso algum erro seja encontrado, o sistema retorna o erro em um formato 
      específico seguindo a rfc 7807. Caso não haja erros, o sistema retorna a mensagem de sucesso. Verifique nos exemplos a seguir o formato da mensagem.

      Exemplos:

      >>> curl -d '{'type': 'Polygon', 'coordinates': [[[1, 2], [3, 4]]]}' -H "Content-Type: application/json" -X POST http://localhost:3000/data
      {
            "detail": "geometry requires more points\n",
            "status": 400,
            "title": "A requisição não pode ser processada devido a erros de geometria, geometria inválida!",
            "type": "https://dominio.visiona/example-error"
      }



.. automodule:: app
   :members:
   :undoc-members:
   :show-inheritance:
