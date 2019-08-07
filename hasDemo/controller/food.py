from werkzeug.wrappers import Response


def actionIndex(request):
    print('Index')
    return Response("Index")

def actionHello(request):
    x = 1
    print('Hello')
    return Response("hello")