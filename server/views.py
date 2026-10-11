import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Car Dealership</title>
        </head>
        <body>
            <h1>Welcome to Car Dealership</h1>
            <p>Find your next car with us.</p>
            <p>The Django application is running.</p>
            <a href="/admin/">Admin</a>
        </body>
        </html>
    """) 

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request,
        username=data.get("username", ""),
        password=data.get("password", ""),
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid username or password"},
            status=401,
        )

    login(request, user)
    response = JsonResponse({
        "message": "Login successful",
        "username": user.username,
    })
    response.set_cookie("sessionid", request.session.session_key)
    return response


@csrf_exempt
def logout_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in"}, status=401)

    username = request.user.username
    logout(request)

    return JsonResponse({
        "message": "Logout successful",
        "username": username,
    })