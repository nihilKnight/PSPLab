class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://easyweb_admin:Ea5yweb_aDm1n@localhost/easyweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'static/uploads/'
