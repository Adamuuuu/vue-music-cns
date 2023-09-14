
from app import create_app



app=create_app()

app.run(debug=app.config['DEBUG'],host=app.config['HOST'],port=app.config['PORT'])