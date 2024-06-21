#!/usr/bin/env python3
"""
Server class to paginate a database of popular baby names.
"""
import csv
from typing import Dict, List, Tuple, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize a new instance of the `Server` class.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Get the cached dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple[int, int]:
        """Calculate the start and end index range for a given page and page size.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            Tuple[int, int]: The start and end index range.
        """
        start_index_next_page: int = page * page_size
        return start_index_next_page - page_size, start_index_next_page

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get the items for a given page number and page size.

        Args:
            page (int): The page number. Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            List[List]: The items for the given page number and page size.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start_index, end_index = self.index_range(page, page_size)
        return self.dataset()[start_index:end_index]

    def get_hyper(self, page: int, page_size: int) -> Dict[str, Union[int, List[List], None]]:
        """Get the items for a given page number and page size with hypermedia.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Union[int, List[List], None]]: A dictionary of the following:
                * page_size (int): The number of items per page.
                * page (int): The page number.
                * data (List[List]): The items for the current page.
                * next_page (int | None): The next page number or None if no more pages.
                * prev_page (int | None): The previous page number or None if no previous pages.
                * total_pages (int): The total number of pages.
        """
        data = self.get_page(page, page_size)
        total_rows: int = len(self.dataset())
        prev_page: int | None = page - 1 if page > 1 else None
        next_page: int | None = page + 1
        if self.index_range(page, page_size)[1] >= total_rows:
            next_page = None
        total_pages: float = total_rows / page_size
        if total_pages % 1 != 0:
            total_pages += 1
        return {'page_size': len(data), 'page': page,
                'data': data, 'next_page': next_page,
                'prev_page': prev_page, 'total_pages': int(total_pages)}

