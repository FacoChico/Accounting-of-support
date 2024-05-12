from logistics.exceptions import CategoryAlreadyExistsException, CategoryNotFoundException
from logistics.models import Category


class CategoryService:

    @staticmethod
    def get_all_categories(limit: int = 10, offset: int = 0) -> tuple[list[Category], int]:
        categories: list[Category] = []
        total: int = 0
        try:
            all_categories = Category.objects.all()
            total = all_categories.count()
            for i in range(offset, offset + limit):
                categories.append(all_categories[i])
        except IndexError:
            pass

        return categories, total

    @staticmethod
    def create_category(category_name: str) -> Category:
        if Category.objects.filter(name=category_name).exists():
            raise CategoryAlreadyExistsException

        category = Category(name=category_name)
        category.save()
        return category

    @staticmethod
    def get_category_by_id(category_id: int) -> Category:
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise CategoryNotFoundException

    @staticmethod
    def edit_category_by_id(category_id: int, name: str) -> Category:
        try:
            category_to_change = Category.objects.get(pk=category_id)
            category_to_change.name = name
            category_to_change.save()
            return category_to_change
        except Category.DoesNotExist:
            raise CategoryNotFoundException

    @staticmethod
    def delete_category_by_id(category_id: int) -> Category:
        try:
            category_to_delete = Category.objects.get(pk=category_id)
            category_to_delete.delete()
            return category_to_delete
        except Category.DoesNotExist:
            raise CategoryNotFoundException
