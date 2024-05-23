from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..exceptions import CategoryNotFoundException, CategoryAlreadyExistsException
from ..serializers.category_serializers import *
from ..services.category_service import CategoryService
from ..repositories import create_database, CategoryRepository


@extend_schema_view(
    post_category=extend_schema(
        summary="Create a new category",
        request=RequestCategorySerializer,
        responses={
            status.HTTP_201_CREATED: ResponseCategorySerializer(),
            status.HTTP_409_CONFLICT: dict,
            status.HTTP_422_UNPROCESSABLE_ENTITY: dict
        }
    ),
    get_categories=extend_schema(
        summary="Get all categories",
        parameters=[
            PaginationSerializer
        ],
        responses={
            status.HTTP_200_OK: ResponseCategoryPageSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: dict
        },
    ),
    get_category_by_id=extend_schema(
        summary="Get category by id",
        responses={
            status.HTTP_200_OK: ResponseCategorySerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict
        },
    ),
    patch_category_by_id=extend_schema(
        summary="Patch category by its id",
        request=RequestCategorySerializer,
        responses={
            status.HTTP_200_OK: ResponseCategorySerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict,
            status.HTTP_422_UNPROCESSABLE_ENTITY: dict
        },
    ),
    delete_category_by_id=extend_schema(
        summary="Delete category by its id",
        responses={
            status.HTTP_200_OK: ResponseCategorySerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict
        },
    )
)
class CategoryViewSet(ViewSet):
    category_db_path = create_database()
    category_repository = CategoryRepository(db_path=category_db_path)
    category_service = CategoryService(category_repository)

    @action(detail=False, methods=["POST"])
    def post_category(self, request):
        in_category = RequestCategorySerializer(data=request.data)
        if not in_category.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=in_category.errors
            )

        category_name = in_category.data.get('name')
        try:
            out_category = self.category_service.create_category(category_name)
            return Response(
                status=status.HTTP_201_CREATED,
                data=ResponseCategorySerializer(out_category).data
            )
        except CategoryAlreadyExistsException:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={
                    "message": f"Category {category_name} already exists"
                }
            )

    @action(detail=False, methods=["GET"])
    def get_categories(self, request):
        query_ser = PaginationSerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        categories, total = self.category_service.get_all_categories(**query_ser.data)
        return Response(
            status=status.HTTP_200_OK,
            data=ResponseCategoryPageSerializer({
                'categories': categories,
                'total': total
            }).data
        )

    @action(detail=False, methods=["GET"])
    def get_category_by_id(self, request, category_id=None):
        try:
            category = self.category_service.get_category_by_id(category_id)
            return Response(
                status=status.HTTP_200_OK,
                data=ResponseCategorySerializer(category).data
            )
        except CategoryNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Category with id={category_id} not found"
                }
            )

    @action(detail=False, methods=["PATCH"])
    def patch_category_by_id(self, request, category_id=None):
        in_category = RequestCategorySerializer(data=request.data)

        if not in_category.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=in_category.errors
            )

        try:
            category = self.category_service.edit_category_by_id(category_id, **in_category.data)
            return Response(
                status=status.HTTP_200_OK,
                data=ResponseCategorySerializer(category).data
            )
        except CategoryNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Category with id={category_id} not found"
                }
            )

    @action(detail=False, methods=["DELETE"])
    def delete_category_by_id(self, request, category_id=None):
        try:
            category = self.category_service.delete_category_by_id(category_id)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": f"Category {category.name} deleted"
                }
            )
        except CategoryNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Category with id={category_id} not found"
                }
            )
