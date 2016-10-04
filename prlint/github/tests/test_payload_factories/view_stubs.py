from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def view(request):
    """
    Testing stub view to return Request's data and GitHub event header.
    """
    return Response({
        'header_github_event': request.META.get('HTTP_X_GITHUB_EVENT', ''),
        'request_data': request.data,
    })
