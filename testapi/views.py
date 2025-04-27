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
        from utils.test_runner import run_test_case
        test_cases = TestCase.objects.all()
        results = []
        
        for case in test_cases:
            try:
                result = run_test_case(case)
                results.append({
                    'id': case.id,
                    'name': case.name,
                    'status': 'success',
                    'response': result
                })
            except Exception as e:
                results.append({
                    'id': case.id,
                    'name': case.name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return Response({
            'total': len(results),
            'passed': len([r for r in results if r['status'] == 'success']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'results': results
        })

    @action(detail=True, methods=['post'])
    def run(self, request, id=None):
        # TODO: 实现执行单个测试用例的逻辑
        return Response({'status': f'Test case {id} executed'})
