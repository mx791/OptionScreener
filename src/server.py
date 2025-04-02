from waitress import serve
from main import app

print("Serving App...")
serve(app.server)