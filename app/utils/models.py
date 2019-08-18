from typing import Optional, List, Any, Union

from asyncpg import Connection, Record

from app.utils.exceptions import ManagerTableDoesNotSpecified

__all__ = ['ModelManager']


class ModelMetaClass(type):

    def __new__(mcs, name, bases, attrs):
        new_class = super(ModelMetaClass, mcs).__new__(mcs, name, bases, attrs)
        new_class._meta = getattr(new_class, 'Meta')
        # if not getattr(new_class._meta, 'db_table'):
        #     raise ManagerTableDoesNotSpecified()
        return new_class


class ModelManager(metaclass=ModelMetaClass):
    def __init__(self, conn: Connection):
        self.__conn = conn

    @property
    def table_name(self):
        return self._meta.db_table

    async def fetch_all(self, *, offset: Optional[int] = 0, limit: Optional[int] = 100) -> List[Record]:
        """Fetch rows without selection"""
        query = f"""
            SELECT *
            FROM {self.table_name}
            LIMIT {limit}
            OFFSET {offset}
        """
        return await self.__conn.fetch(query)

    async def fetch_by(self, key: str, value: Any, *, offset: Optional[int] = 0,
                       limit: Optional[int] = 1) -> Union[Record, List[Record]]:
        """Fetch rwo or rows by single selection"""
        query = f"""
            SELECT *
            FROM {self.table_name}
            WHERE {key} = $1
            LIMIT {limit}
            OFFSET {offset}
        """
        if limit == 1:
            return await self.__conn.fetchrow(query, value)
        else:
            return await self.__conn.fetch(query, value)

    async def insert_value(self, **kwargs: Any) -> None:
        """Insert single object"""
        values_args = kwargs.values()
        values_args_len = len(values_args)
        query = f"""
            INSERT INTO {self.table_name}
            ({', '.join(key for key in kwargs.keys())})
            VALUES ({self._generate_indexes(values_args_len)})
        """
        await self.__conn.execute(query, *values_args)

    @staticmethod
    def _generate_indexes(count: int, offset: int = 0) -> str:
        """Generate strings like '$1, $2, $3' for inserting args into query"""
        index_list = [f'${i + offset + 1}' for i in range(count)]
        return ', '.join(index_list)

    class Meta:
        db_table = None  # Must override in sub manager
