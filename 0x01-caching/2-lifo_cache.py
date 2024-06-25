#!/usr/bin/python3

from threading import RLock

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    Implementation of a Last In First Out caching system.
    """

    def __init__(self):
        """
        Instantiate a new LIFOCache object.
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """
        Add an item to the cache. If the cache is at its maximum size, the
        earliest item is discarded.

        Args:
            key (Hashable): The key of the item.
            item: The item to be added.
        """
        if key is not None and item is not None:
            rem_key = self._balance(key)
            with self.__rlock:
                self.cache_data.update({key: item})
            if rem_key is not None:
                print('DISCARD: {}'.format(rem_key))

    def get(self, key):
        """
        Retrieve an item from the cache by key.

        Args:
            key (Hashable): The key of the item to retrieve.

        Returns:
            The value of the item if it exists in the cache, None otherwise.
        """
        with self.__rlock:
            return self.cache_data.get(key, None)

    def _balance(self, key_add):
        """
        Remove the earliest item from the cache at MAX size.

        Args:
            key_add (Hashable): The key of the new item.

        Returns:
            The key of the removed item, or None if no item was removed.
        """
        rem_key = None
        with self.__rlock:
            all_keys = len(self.__keys)
            if key_add not in self.__keys:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    rem_key = self.__keys.pop(all_keys - 1)
                    self.cache_data.pop(rem_key)
            else:
                self.__keys.remove(key_add)
            self.__keys.insert(all_keys, key_add)
        return rem_key
