from flask import Flask
from celery import Celery


# 使用函数定义Celery对象
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery


# 将Flask实例化，生成对象app
app = Flask(__name__)
# 设置app的配置信息
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    # 解决Json乱码
    JSON_AS_ASCII=False
)
# 将Flask与Celery绑定
celery = make_celery(app)
