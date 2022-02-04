import pickle
from typing import Any, Union
from datetime import datetime


class DataStorage:

    _DataStorageObj = None

    def __new__(cls, *args, **kwargs):
        if cls._DataStorageObj is None:
            cls._DataStorageObj = super().__new__(cls)
        return cls._DataStorageObj

    def __init__(self):
        self.path = r"word_dump"
        self._catalogue = []
        self._data: dict[str, Any] = {}
        self._setup()

    def _setup(self):
        self._data = self._data_storage_handler()
        if self._data['creation'] != datetime.today().strftime('%Y-%m-%d'):
            self._data.clear()
            self._data['creation'] = datetime.today().strftime('%Y-%m-%d')
            self._data_storage_handler(self._data)

    def _data_storage_handler(self, obj_to_store=None) -> Union[dict[str, Any], None]:
        if obj_to_store is not None:
            with open(self.path, "wb") as handle:
                pickle.dump(obj_to_store, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
        else:
            try:
                with open(self.path, 'rb') as handle:
                    return pickle.load(handle)
            except FileNotFoundError:
                with open(self.path, 'wb') as handle:
                    pickle.dump({}, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return {"creation": datetime.today().strftime('%Y-%m-%d')}

    def store_object(self, code: int, words):
        self._data[code] = words
        self._data_storage_handler(self._data)

    def load_object(self, code: int):
        yield from self._data.setdefault(code, None)

    def remove(self, *names):
        for name in names:
            del self._data[name]

    def __getitem__(self, key):
        return self._data[key]

    def saved(self, item):
        return item in self._data

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        return item in self._data
