import moduleTemplate

module_id = "fuck_module"

def temp(params: dict):
    print(params)
    return params

def test():
    print(time)

moduleTemplate.init(5000, module_id, [['get', '/get', temp], ['put', '/put', temp], ['post', '/post', temp], ['delete', '/delete', temp], ['get', '/model-time', test]])

print("fuck_off")