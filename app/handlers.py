import models
from fastapi import Request, HTTPException


async def get_games():
    """
    Getting a list of all games with information about its users
    :return:
    """
    try:
        response = await models.Game.get_all_games()
        return response
    except Exception as e:
        raise HTTPException(404, e)


async def connect_to_game(
        user_id: int,
        game_id: int
):
    """
    Connecting to certain game (creating new User - Game object)
    :param user_id:
    :param game_id:
    :return:
    """
    try:
        await models.User.connect_to_game(user_id=user_id, game_id=game_id)

        return {"message": "User successfully connected to the game!"}
    except Exception as e:
        raise HTTPException(404, e)


async def user_detail(user_id: int):
    """
    Getting all information about certain user and its games
    :param user_id:
    :return:
    """
    try:
        response = await models.User.get_current_user(user_id=user_id)

        return response
    except Exception as e:
        raise HTTPException(404, e)

