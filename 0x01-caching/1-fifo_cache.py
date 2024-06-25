#!/usr/bin/python3
"""This module implements a First In First Out cache."""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    Implements a First In First Out cache.
    """

    def __init__(self):
        """Initializes the cache."""
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """Adds an item to the cache.

        If the cache is at its maximum size, the earliest item is discarded.

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
        """Gets an item from the cache.

        Args:
            key (Hashable): The key of the item.

        Returns:
            The item, or None if the item is not in the cache.
        """
        with self.__rlock:
            return self.cache_data.get(key, None)

    def _balance(self, key_add):
        """Removes the oldest item from the cache at MAX size.

        Args:
            key_add (Hashable): The key of the new item.

        Returns:
            The key of the removed item, or None if no item was removed.
        """
        rem_key = None
        with self.__rlock:
            if key_add not in self.__keys:
                all_keys = len(self.__keys)
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    rem_key = self.__keys.pop(0)
                    self.cache_data.pop(rem_key)
                self.__keys.insert(all_keys, key_add)
        return rem_key
