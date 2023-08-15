from abc import ABC, abstractmethod
from helpers import constants
import math
import pandas as pd
from typing import Callable, Union, List

class AbstractPaginatedTable(ABC):
    page = 0
    total_pages = 0

    @abstractmethod
    def page_footer(self) -> str:
        pass
    
    @abstractmethod
    def num_page_first_entry(self) -> int:
        pass

    @abstractmethod
    def num_page_last_entry(self) -> int:
        pass

    @abstractmethod
    def jump_page(self, offset: int) -> pd.DataFrame:
        pass

    def can_pprev(self) -> bool:
        return False if self.page + constants.Format.WOWS_SIZE_PPREV.value < 0 else True
    
    def can_prev(self) -> bool:
        return False if self.page + constants.Format.WOWS_SIZE_PREV.value < 0 else True

    def can_next(self) -> bool:
        return False if self.page + constants.Format.WOWS_SIZE_NEXT.value >= self.total_pages else True
    
    def can_nnext(self) -> bool:
        return False if self.page + constants.Format.WOWS_SIZE_NNEXT.value >= self.total_pages else True

class PaginatedDF(AbstractPaginatedTable):
    page, per_row = 0, 0
    total_entries, total_pages = 0, 0
    meta, data = None, None
    title_function, parse_function = None, None

    def __init__(self, meta: dict, data: Union[list, pd.DataFrame], title_function: Callable, parse_function: Callable):
        self.page = 0
        self.per_row = constants.Format.WOWS_DEFAULT_PAGE_SIZE.value
        self.meta = meta
        self.data = data
        self.total_entries = meta['count']
        self.total_pages = math.ceil(self.total_entries / self.per_row)
        self.title_function = title_function
        self.parse_function = parse_function

    def page_footer(self) -> str:
        return (
            f"Showing page {self.page+1} of {self.total_pages} " +
            f"({self.num_page_first_entry()+1}-{self.num_page_last_entry()+1} of {self.total_entries} results)"
        )
    
    def num_page_first_entry(self):
        return self.page*self.per_row

    def num_page_last_entry(self):
        return min((self.page+1)*self.per_row, self.total_entries) - 1

    def jump_page(self, offset: int) -> pd.DataFrame:
        self.page += offset
        return self.data.iloc[self.num_page_first_entry() : self.num_page_last_entry()+1]
    
class CustomPaginatedDF(AbstractPaginatedTable):
    page = 0
    total_pages = 0
    meta, data = None, None
    title_function, parse_function = None, None

    def __init__(self, meta: dict, data: Union[list, pd.DataFrame], title_function: Callable, parse_function: Callable):
        self.page = 0
        self.meta = meta
        self.data = data
        self.total_pages = len(data)
        self.title_function = title_function
        self.parse_function = parse_function

    def page_footer(self) -> str:
        return (
            f"Showing page {self.page+1} of {self.total_pages}"
        )

    def jump_page(self, offset: int) -> pd.DataFrame:
        self.page += offset
        return self.data[self.page]
        
    def num_page_first_entry(self) -> int:
        pass
        
    def num_page_last_entry(self) -> int:
        pass