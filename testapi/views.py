from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TestCase
from .serializers import TestCaseSerializer
import json

class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['post'])
    def upload(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        try:
            data = json.load(file)
            if isinstance(data, list):
                for item in data:
                    serializer = self.get_serializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def run_all(self, request):
        # TODO: 实现执行所有测试用例的逻辑
        return Response({'status': 'All test cases executed'})

    @action(detail=True, methods=['post'])
    def run(self, request, id=None):
        # TODO: 实现执行单个测试用例的逻辑
        return Response({'status': f'Test case {id} executed'})
