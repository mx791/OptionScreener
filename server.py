from waitress import serve
from main import app

serve(app.server)