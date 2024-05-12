from logistics.exceptions import LogisticsNotFoundException, CategoryNotFoundException
from logistics.models import Logistics, Category


class LogisticsService:
    @staticmethod
    def get_all_logistics(limit: int = 10, offset: int = 0, category_id: int = None) -> tuple[list[Logistics], int]:
        logistics: list[Logistics] = []
        total: int = 0
        try:
            if category_id is not None:
                all_logistics = Logistics.objects.filter(category_id=category_id)
            else:
                all_logistics = Logistics.objects.all()

            total = all_logistics.count()
            for i in range(offset, offset + limit):
                logistics.append(all_logistics[i])
        except IndexError:
            pass

        return logistics, total

    @staticmethod
    def create_logistics(name: str, category_id: int, type: str, price: int, quantity_available: int) -> Logistics:
        try:
            category = Category.objects.get(pk=category_id)
            logistics = Logistics(name=name, category=category,
                                  type=type, price=price, quantity_available=quantity_available)
            logistics.save()
            return logistics
        except Category.DoesNotExist:
            raise CategoryNotFoundException

    @staticmethod
    def get_logistics_by_id(logistics_id: int) -> Logistics:
        try:
            return Logistics.objects.get(pk=logistics_id)
        except Logistics.DoesNotExist:
            raise LogisticsNotFoundException

    @staticmethod
    def edit_logistics_by_id(logistics_id: int, name: str, category_id: int,
                             type: str, price: int, quantity_available: int) -> Logistics:
        try:
            logistics_to_change = Logistics.objects.get(pk=logistics_id)
            logistics_to_change.name = name
            logistics_to_change.category = Category.objects.get(pk=category_id)
            logistics_to_change.type = type
            logistics_to_change.price = price
            logistics_to_change.quantity_available = quantity_available
            logistics_to_change.save()
            return logistics_to_change
        except Logistics.DoesNotExist:
            raise LogisticsNotFoundException
        except Category.DoesNotExist:
            raise CategoryNotFoundException

    @staticmethod
    def delete_logistics_by_id(logistics_id: int) -> Logistics:
        try:
            logistics_to_delete = Logistics.objects.get(pk=logistics_id)
            logistics_to_delete.delete()
            return logistics_to_delete
        except Logistics.DoesNotExist:
            raise LogisticsNotFoundException
