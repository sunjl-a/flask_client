from flask import request, jsonify
from taskInfo import *


@app.route('/')
def task_receive():
    taskId = request.args.get('taskId', '')
    name = request.args.get('name', '')
    kwargs = {}
    kwargs['train_date'] = '2019-08-31'
    kwargs['from_station'] = '信阳'
    kwargs['to_station'] = '北京'
    AutoTask.delay(taskId, name, **kwargs)
    return jsonify({"result": "success",
                    "taskID": taskId,})


if __name__ == '__main__':
    app.run(port=8000, debug=True)
