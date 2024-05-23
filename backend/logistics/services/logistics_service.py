from ..exceptions import LogisticsNotFoundException, CategoryNotFoundException
from ..models import Logistics
from ..repositories import LogisticsRepository


class LogisticsService:
    def __init__(self, repo: LogisticsRepository):
        self.repo = repo

    def get_all_logistics(self, limit: int = 10, offset: int = 0,
                          category_id: int = None) -> tuple[list[Logistics], int]:
        logistics: list[Logistics] = []
        total: int = 0
        try:
            all_logistics = self.repo.get_all(category_id=category_id)

            total = len(all_logistics)
            for i in range(offset, offset + limit):
                logistics.append(all_logistics[i])
        except IndexError:
            pass

        return logistics, total

    def create_logistics(self, name: str, category_id: int,
                         type: str, price: int, quantity_available: int) -> Logistics:
        category = self.repo.get_category(category_id)
        if category is None:
            raise CategoryNotFoundException
        logistics = self.repo.add(name=name, category_id=category_id,
                              type=type, price=price, quantity_available=quantity_available)
        return logistics

    def get_logistics_by_id(self, logistics_id: int) -> Logistics:
        logistics = self.repo.get_by_id(logistics_id)
        if logistics is None:
            raise LogisticsNotFoundException
        return logistics

    def edit_logistics_by_id(self, logistics_id: int, name: str, category_id: int,
                             type: str, price: int, quantity_available: int) -> Logistics:
        if self.repo.get_category(category_id) is None:
            raise CategoryNotFoundException
        logistics_to_change = self.repo.update(logistics_id, name=name, category_id=category_id,
                         type=type, price=price, quantity_available=quantity_available)
        if logistics_to_change is None:
            raise LogisticsNotFoundException
        return logistics_to_change

    def delete_logistics_by_id(self, logistics_id: int) -> Logistics:
        logistics_to_delete = self.repo.delete(logistics_id)
        if logistics_to_delete is None:
            raise LogisticsNotFoundException
        return logistics_to_delete

