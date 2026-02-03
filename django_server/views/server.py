from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


def health_check_view(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdminRootRedirectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return redirect("/admin/")
