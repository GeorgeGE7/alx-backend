#!/usr/bin/env python3
"""
Resilient hypermedia pagination
"""

import csv
from typing import Dict, List


class Server:
    """
    Server class to paginate a database of popular baby names.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """
        Initialize a new instance of the Server class.
        """
        self.__indexed_dataset = None
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Get the cached dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                self.__dataset = [row for row in reader][1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Get the dataset indexed by sorting position, starting at 0.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int | None = None, page_size: int = 10) -> Dict:
        """
        Get the items for a given index and page size with hypermedia.

        Args:
            index (int): The start index of the current page.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Union[int, List[List], None]]: A dictionary of the following:
                * page_size (int): The number of items per page.
                * index (int): The start index of the current page.
                * data (List[List]): The items for the current page.
                * next_index (int | None): The next index or None if no more pages.
        """
        dataset = self.indexed_dataset()
        check = []
        index = 0 if index is None else index
        keys = sorted(dataset.keys())
        assert index >= 0 and index <= keys[-1]
        check = [i for i in keys if i >= index and len(check) <= page_size]
        data = [dataset[i] for i in check[:-1]]
        next_index = check[-1] if len(check) - page_size == 1 else None
        return {'page_size': len(data), 'index': index,
                'data': data, 'next_index': next_index}

