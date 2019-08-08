from werkzeug.wrappers import Response

def actionIndex(request):
    return Response("Main")