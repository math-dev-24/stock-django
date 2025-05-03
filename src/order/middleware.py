from .models import Company
import uuid


class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        company_id = request.session.get('company_id')

        if company_id:
            try:
                company_id = uuid.UUID(company_id)
                request.current_company = Company.objects.get(id=company_id)
            except:
                request.current_company = None
        else:
            request.current_company = None

        if request.current_company is None and request.user.is_authenticated:
            request.current_company = request.user.company_members.first()
        request.list_company = Company.objects.all()

        response = self.get_response(request)

        return response
