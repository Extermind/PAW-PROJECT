from flask import Flask, render_template
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your Flask Application"
    }
)

@swagger_bp.route(SWAGGER_URL)
def swagger_ui():
    return render_template('swaggerui.html', spec_url='/swagger.yaml')
