

async def test_index_page(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.json() == {'app': 'aiohttp-template'}


async def test_health_page(cli):
    resp = await cli.get('/health/')
    assert resp.status == 200
    assert await resp.json() == {
        'db': 'ok',
        'redis': 'ok',
    }
