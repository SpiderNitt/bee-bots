from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager
from chain import BlockChain
from jsonrpc import Dispatcher

d = Dispatcher()
chain = BlockChain()
d.add_method(chain.add_block, name="add_block")
d.add_method(chain.get_block, name="get_block")


def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    # dispatcher["echo"] = lambda s: s
    # dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(request.data, d)
    return Response(response.json, mimetype="application/json")


if __name__ == "__main__":
    run_simple("localhost", 4000, application)

