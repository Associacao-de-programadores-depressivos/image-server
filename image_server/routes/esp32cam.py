from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def main(req: web.Request):
    return web.Response(text="Image Server is running!")
