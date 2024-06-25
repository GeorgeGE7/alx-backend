#!/usr/bin/python3
"""This module implements MRU Cache Replacement Implementation Class."""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    An implementation of MRU(Most Recently Used) Cache.

    This class maintains a dictionary of cached items and a list of keys in
    the order they were accessed, with the most recently accessed item at the
    end of the list. When a new item is added to the cache, the oldest item
    is discarded if the cache is at its maximum size. 

    Attributes:
        __keys (list): Stores cache keys from least to most accessed.
        __rlock (RLock): Lock accessed resources to prevent race condition.
    """
    def __init__(self):
        """
        Instantiation method, sets instance attributes.
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """
        Add an item in the cache.

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
        Get an item by key.

        Args:
            key (Hashable): The key of the item.

        Returns:
            The value of the item in the cache, or None if the item is not in
            the cache.
        """
        with self.__rlock:
            value = self.cache_data.get(key, None)
            if key in self.__keys:
                self._balance(key)
        return value

    def _balance(self, key_add):
        """
        Removes the earliest item from the cache at MAX size.

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

