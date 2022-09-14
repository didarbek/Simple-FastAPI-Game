import handlers

from fastapi import APIRouter, status


def init(app):
    router = APIRouter(tags=['Simple Game'])

    router.add_api_route(
        '/games/',
        methods=['GET'],
        status_code=status.HTTP_200_OK,
        endpoint=handlers.get_games,
        tags=['API', 'Games']
    )
    router.add_api_route(
        '/connect/{user_id}/{game_id}/',
        methods=['GET'],
        status_code=status.HTTP_200_OK,
        endpoint=handlers.connect_to_game,
        tags=['API', 'Games']
    )
    router.add_api_route(
        '/user/{user_id}/',
        methods=['GET'],
        status_code=status.HTTP_200_OK,
        endpoint=handlers.user_detail,
        tags=['API', 'Users']
    )

    app.include_router(router)
