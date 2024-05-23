from ..exceptions import CategoryAlreadyExistsException, CategoryNotFoundException
from ..models import Category
from ..repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, repository: CategoryRepository):
        self.repo = repository

    def get_all_categories(self, limit: int = 10, offset: int = 0) -> tuple[list[Category], int]:
        categories: list[Category] = []
        total: int = 0
        try:
            all_categories = self.repo.get_all()
            total = len(all_categories)
            for i in range(offset, offset + limit):
                categories.append(all_categories[i])
        except IndexError:
            pass

        return categories, total

    def create_category(self, category_name: str) -> Category:
        if self.repo.get_by_name(category_name):
            raise CategoryAlreadyExistsException

        return self.repo.add(category_name)

    def get_category_by_id(self, category_id: int) -> Category:
        category = self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException
        return category

    def edit_category_by_id(self, category_id: int, name: str) -> Category:
        category_to_change = self.repo.update(category_id, name)
        if not category_to_change:
            raise CategoryNotFoundException

        return category_to_change

    def delete_category_by_id(self, category_id: int) -> Category:
        category_to_delete = self.repo.delete(category_id)
        if not category_to_delete:
            raise CategoryNotFoundException

        return category_to_delete
