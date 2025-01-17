from django.http import HttpResponseRedirect

class CustomMiddleware:

    # One time initialisation
    def __init__(self, get_response):
        self.get_response = get_response

    # Code to be executed for each request before the view is called
    def __call__(self, request):
        print("Middleware executed")
        open_urls = ['/','/signup/']
        session = request.session.get('user')
        if request.path not in open_urls and not session:
            print("Redirecting to login page")
            return HttpResponseRedirect('/')
        elif request.path in open_urls and session:
            print("Redirecting to tweet page")
            return HttpResponseRedirect('/skill/')
            
        response = self.get_response(request)
        return response