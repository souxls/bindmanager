#-*-coding:utf8-*-
from application import app
app.run(debug=app.config.get('DEBUG'), host=app.config.get('HOST'), \
       port=app.config.get('PORT'), processes=app.config.get('PROCESSES'))
