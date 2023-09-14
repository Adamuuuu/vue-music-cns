
import  os
from flask import Flask

def create_app(config=None):
    app=Flask(__name__)
# 读取config-setting的配置将其存入app.config这个字典
    app.config.from_object('config.setting')

    # 根据系统环境变量加载， 可以保密 加载不同的配置文件
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')

    if config is not None:
        if isinstance(config,dict):
            app.config.update(config)
        elif config.endswith(".py"):
            app.config.from_pyfile(config)

    import router
    router.init_app(app)
    import model
    model.init_db_app(app)
    return app