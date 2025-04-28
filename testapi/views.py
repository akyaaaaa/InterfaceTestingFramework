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
            # 多条
            if isinstance(data, list):
                for item in data:
                    serializer = self.get_serializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
            # 单条
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'{str(e)},上传文件只能为json文件，多条用例用[]包含'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def run_all(self, request):
        
        from utils.concurrent_runner import run_concurrently
        test_cases = TestCase.objects.all()
        results = run_concurrently(test_cases)

        return Response({
            'total': len(results),
            'passed': len([r for r in results if r['status'] == 'success']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'results': results
        })

    @action(detail=True, methods=['post'])
    def run(self, request, id=None):
        """执行单个测试用例 /api/testcases/{id}/run/"""
        # get_object 的默认实现会根据 URL 中的主键（pk）或 slug 字段查找对应的模型实例,故不用赋值
        case = self.get_object()
        from utils.test_runner import run_test_case
        try:
            result = run_test_case(case)
            return Response({
                'id': case.id,
                'name': case.name,
                'status': 'success',
                'response': result
            })
        except Exception as e:
            return Response({
                'id': case.id,
                'name': case.name,
                'status': 'failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_from_json(self, request):
        """从JSON数据创建测试用例"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
