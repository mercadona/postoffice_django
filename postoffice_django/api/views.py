from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import BaseDeleteView

from postoffice_django.models import PublishingError
from postoffice_django.serializers import MessagesSerializer


class ListMessagesView(View):
    DEFAULT_MAX_RESULTS = 100

    def get(self, request, *args, **kwargs):
        max_results = self._get_max_results(request)
        messages = PublishingError.objects.order_by('created_at')[:max_results]
        data = MessagesSerializer().serialize(messages)
        return JsonResponse(data, safe=False)

    def _get_max_results(self, request):
        return int(request.GET.get('limit', self.DEFAULT_MAX_RESULTS))


@method_decorator(csrf_exempt, name='dispatch')
class DeleteMessageView(BaseDeleteView):
    queryset = PublishingError.objects.all()

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        message.delete()
        return HttpResponse(status=204)
