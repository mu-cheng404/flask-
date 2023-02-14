#配置文件
SECRET_KEY= "sajfasjkfaksjfbajb"
#数据库配置文件
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "flask_demo"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

# gbeechqjuyjldebh 邮箱授权码
#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
# MAIL_USE_TLS : 默认为 False
MAIL_USE_SSL = True
# MAIL_DEBUG : 默认为 app.debug
MAIL_USERNAME = "muzithe@qq.com"
MAIL_PASSWORD = "gbeechqjuyjldebh"
MAIL_DEFAULT_SENDER = "muzithe@qq.com"
# MAIL_MAX_EMAILS : 默认为 None
# MAIL_SUPPRESS_SEND : 默认为 app.testing
# MAIL_ASCII_ATTACHMENTS : 默认为 False

