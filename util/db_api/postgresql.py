import logging
from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from asyncpg.exceptions import UniqueViolationError
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetch_val: bool = False,
                      fetch_row: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetch_val:
                    result = await connection.fetchval(command, *args)
                elif fetch_row:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );        
        """

        await self.execute(sql, execute=True)

    async def create_table_links(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Links (
        id SERIAL PRIMARY KEY,
        code VARCHAR(100) NOT NULL,
        admin_id INT REFERENCES Admins (id) ON DELETE CASCADE UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_shortcuts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Shortcuts (
        id SERIAL PRIMARY KEY,
        short VARCHAR(255) NOT NULL UNIQUE,
        full_text TEXT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def drop_table_admins(self):
        sql = "DROP TABLE Admins CASCADE"
        await self.execute(sql, execute=True)

    async def drop_table_links(self):
        sql = "DROP TABLE Links"
        await self.execute(sql, execute=True)

    async def drop_table_shortcuts(self):
        sql = "DROP TABLE Shortcuts"
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_all_admins(self):
        sql = "SELECT * FROM Admins"
        await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch_row=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Admins"
        return await self.execute(sql, fetch_val=True)

    async def add_admin(self, full_name: str, username: str, telegram_id: int):
        sql = "INSERT INTO Admins (full_name, username, telegram_id) VALUES ($1, $2, $3)"
        parameters = (full_name, username, telegram_id)
        try:
            await self.execute(sql, *parameters, execute=True)
        except UniqueViolationError:
            logging.error(f"UniqueViolationError: Admin '{username}' already exists")

    async def check_admin(self, telegram_id):
        sql = "SELECT EXISTS(SELECT * FROM Admins WHERE telegram_id=$1)"
        return await self.execute(sql, telegram_id, fetch_val=True)

    async def get_admins(self):
        sql = "SELECT telegram_id FROM Admins"
        return await self.execute(sql, fetch=True)

    async def add_link(self, code: str, admin_id: int):
        sql = "INSERT INTO Links (code, admin_id) VALUES ($1, $2)"
        parameters = (code, admin_id)
        try:
            await self.execute(sql, *parameters, execute=True)
            return True
        except UniqueViolationError:
            logging.error(f"UniqueViolationError: Admin '{admin_id}' already has ref link")
            return False

    async def select_link(self, **kwargs):
        sql = "SELECT * FROM Links WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch_row=True)

    async def delete_link(self, code: str, admin_id: int):
        sql = "DELETE FROM Links WHERE code=$1 AND admin_id=$2"
        parameters = (code, admin_id)
        await self.execute(sql, *parameters, execute=True)

    async def get_admin_link(self, admin_id: int):
        sql = "SELECT * FROM Links WHERE admin_id=$1"
        return await self.execute(sql, admin_id, fetch_row=True)

    async def add_shortcut(self, short: str, full: str):
        sql = "INSERT INTO Shortcuts (short, full_text) VALUES ($1, $2)"
        parameters = (short, full)
        try:
            await self.execute(sql, *parameters, execute=True)
            return True
        except UniqueViolationError:
            logging.error(f"UniqueViolationError: f '{short}' already exists")
            return False

    async def select_shortcut(self, **kwargs):
        sql = "SELECT * FROM Shortcuts WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch_row=True)
