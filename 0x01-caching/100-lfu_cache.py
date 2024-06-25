#!/usr/bin/python3
"""Least Frequently Used Cache Implementation.

This class implements the Least Frequently Used (LFU) caching algorithm.

"""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    An implementation of LFU Cache.

    Attributes:
        __stats (dict): A dictionary of cache keys for access count.
        __rlock (RLock): Lock accessed resources to prevent race condition.
    """
    def __init__(self):
        """ Initialize the LFU Cache.
        """
        super().__init__()
        self.__stats = {}
        self.__rlock = RLock()

    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key (Hashable): The key of the item.
            item: The item to be added.
        """
        if key is not None and item is not None:
            rem_key = self._balance(key)
            with self.__rlock:
                self.cache_data[key] = item
            if rem_key is not None:
                print('DISCARD: {}'.format(rem_key))

    def get(self, key):
        """
        Get an item from the cache.

        Args:
            key (Hashable): The key of the item.

        Returns:
            The item associated with the key.
        """
        with self.__rlock:
            value = self.cache_data.get(key)
            if key in self.__stats:
                self.__stats[key] += 1
        return value

    def _balance(self, key_add):
        """
        Removes the least frequently used item from the cache at MAX size.

        Args:
            key_add (Hashable): The key of the new item.

        Returns:
            The key of the removed item.
        """
        rem_key = None
        with self.__rlock:
            if key_add not in self.__stats:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    rem_key = min(self.__stats, key=self.__stats.get)
                    self.cache_data.pop(rem_key)
                    self.__stats.pop(rem_key)
            self.__stats[key_add] = self.__stats.get(key_add, 0) + 1
        return rem_key
