import asyncpg
import sqlalchemy as sa

from sqlalchemy.orm import relationship

from config.db import adb_session
from config.db_sync import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(79))
    age = sa.Column(sa.Integer(), sa.CheckConstraint('age > 0 AND age < 100'))
    email = sa.Column(sa.String(79))

    users = relationship('Game', secondary='user_games', back_populates='users')

    def __repr__(self):
        return f'User({self.id} - {self.email})'

    @classmethod
    async def get_current_user(cls, user_id: int):
        """
        Getting the data (user details and games he's connected to) about particular user
        :param user_id:
        :return:
        """
        async with adb_session() as conn:
            user = await conn.fetchrow(
                '''
                select * from users
                where users.id = $1
                ''',
                user_id
            )
            games = await conn.fetch(
                '''
                select games.* from games, user_games
                where user_games.game_id = games.id
                and user_games.user_id = $1 
                ''',
                user_id
            )

            if user is None:
                return {'message': 'User doesn\'t exist!'}

            return {'user': user, 'user\'s games': games}

    @classmethod
    async def connect_to_game(
            cls,
            user_id: int,
            game_id: int
    ):
        """
        Connecting to game by providing user's and game's ids
        :param user_id:
        :param game_id:
        :return:
        """
        async with adb_session() as conn:
            return await conn.execute(
                '''
                insert into user_games(user_id, game_id)
                values($1, $2)
                ''',
                user_id,
                game_id
            )


class Game(Base):
    __tablename__ = 'games'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(79))

    users = relationship('User', secondary='user_games', back_populates='games')

    def __repr__(self):
        return f'Game({self.id} - {self.name})'

    @classmethod
    async def get_all_games(cls) -> asyncpg.Record:
        """
        Getting all games from a database
        :return:
        """
        async with adb_session() as conn:
            games = await conn.fetch(
                '''
                select games.*, array_agg(users.email) as users from games, users, user_games
                where user_games.user_id = users.id
                and user_games.game_id = games.id
                group by games.id
                '''
            )

            if games is None:
                return {'message': 'There are no games yet!'}

            return games


class UserGame(Base):
    __tablename__ = 'user_games'

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    game_id = sa.Column(sa.Integer, sa.ForeignKey('games.id'), primary_key=True)

    def __repr__(self):
        return f'UserGame ({self.user_id} - {self.game_id})'
