import taskCreater
import moduleTemplate

taskCreater.init('output.xlsx')
moduleTemplate.init(3333, 'taskCreater', [['get', '/model-time', taskCreater.get_next_flight]])