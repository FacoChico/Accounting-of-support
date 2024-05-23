from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..exceptions import LogisticsNotFoundException, CategoryNotFoundException
from ..serializers.logistics_serializers import *
from ..services.logistics_service import LogisticsService
from ..repositories import create_database, LogisticsRepository


@extend_schema_view(
    post_logistics=extend_schema(
        summary="Create new logistics",
        request=RequestLogisticsSerializer,
        responses={
            status.HTTP_201_CREATED: ResponseLogisticsSerializer(),
            status.HTTP_404_NOT_FOUND: dict,
            status.HTTP_422_UNPROCESSABLE_ENTITY: dict
        }
    ),
    get_logistics=extend_schema(
        summary="Get all logistics",
        parameters=[
            LogisticsPaginationSerializer,
        ],
        responses={
            status.HTTP_200_OK: ResponseLogisticsPageSerializer(many=True)
        },
    ),
    get_logistics_by_id=extend_schema(
        summary="Get logistics by its id",
        responses={
            status.HTTP_200_OK: ResponseLogisticsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict
        },
    ),
    delete_logistics_by_id=extend_schema(
        summary="Delete logistics by its id",
        responses={
            status.HTTP_200_OK: ResponseLogisticsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict
        },
    ),
    patch_logistics_by_id=extend_schema(
        summary="Patch logistics by its id",
        request=RequestLogisticsSerializer,
        responses={
            status.HTTP_200_OK: ResponseLogisticsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: dict
        },
    )
)
class LogisticsViewSet(viewsets.ModelViewSet):
    logistics_db_path = create_database()
    logistics_repository = LogisticsRepository(db_path=logistics_db_path)
    logistics_service = LogisticsService(logistics_repository)

    @action(detail=False, methods=["POST"])
    def post_logistics(self, request):
        in_logistics = RequestLogisticsSerializer(data=request.data)
        if not in_logistics.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=in_logistics.errors
            )

        try:
            out_logistics = self.logistics_service.create_logistics(**in_logistics.data)
            return Response(
                status=status.HTTP_201_CREATED,
                data=ResponseLogisticsSerializer(out_logistics).data
            )
        except CategoryNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Category with id={in_logistics.data.get('category_id')} not found"
                }
            )

    @action(detail=False, methods=["GET"])
    def get_logistics(self, request):
        query_ser = LogisticsPaginationSerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        logistics, total = self.logistics_service.get_all_logistics(**query_ser.data)
        return Response(
            status=status.HTTP_200_OK,
            data=ResponseLogisticsPageSerializer({
                'logistics': logistics,
                'total': total
            }).data
        )

    @action(detail=False, methods=["GET"])
    def get_logistics_by_id(self, request, logistics_id=None):
        try:
            logistics = self.logistics_service.get_logistics_by_id(logistics_id)
            return Response(
                status=status.HTTP_200_OK,
                data=ResponseLogisticsSerializer(logistics).data
            )
        except LogisticsNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Logistics with id={logistics_id} not found"
                }
            )

    @action(detail=False, methods=["PATCH"])
    def patch_logistics_by_id(self, request, logistics_id=None):
        in_logistics = RequestLogisticsSerializer(data=request.data)

        if not in_logistics.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=in_logistics.errors
            )

        try:
            logistics = self.logistics_service.edit_logistics_by_id(logistics_id, **in_logistics.data)
            return Response(
                status=status.HTTP_200_OK,
                data=ResponseLogisticsSerializer(logistics).data
            )
        except LogisticsNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Logistics with id={logistics_id} not found"
                }
            )
        except CategoryNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Category with id={in_logistics.data.get('category_id')} not found"
                }
            )

    @action(detail=False, methods=["DELETE"])
    def delete_logistics_by_id(self, request, logistics_id=None):
        try:
            logistics = self.logistics_service.delete_logistics_by_id(logistics_id)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": f"Logistics {logistics.name} deleted"
                }
            )
        except LogisticsNotFoundException:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": f"Logistics with id={logistics_id} not found"
                }
            )
