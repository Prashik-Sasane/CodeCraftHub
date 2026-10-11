import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Car Dealership</title>

    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            color: #273444;
            background: #fff;
        }

        nav {
            background: #29343d;
            color: white;
            padding: 20px 4%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 18px;
        }

        nav strong { font-size: 27px; }

        nav a {
            color: white;
            text-decoration: none;
            margin-left: 24px;
            font-size: 17px;
        }

        .hero {
            padding: 48px 20px;
            text-align: center;
            background: linear-gradient(135deg, #e5edf3, #b8c9d5);
            color: #101820;
        }

        .hero h1 {
            font-size: clamp(30px, 4vw, 48px);
            margin: 0 0 14px;
        }

        .hero p {
            font-size: 21px;
            margin: 0;
        }

        main { padding: 28px 4%; }

        main h2 {
            font-size: 34px;
            margin: 8px 0 18px;
        }

        .dealers {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
        }

        .card {
            border: 1px solid #d8dde2;
            border-radius: 7px;
            padding: 14px;
            box-shadow: 0 2px 5px #0000000d;
        }

        .photo {
            height: 190px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 27px;
            font-weight: bold;
            background: linear-gradient(140deg, #6b8da6, #243c50);
            text-align: center;
        }

        .card h3 {
            font-size: 23px;
            margin: 12px 0 8px;
        }

        .card p {
            margin: 7px 0;
            line-height: 1.4;
        }

        .website {
            display: inline-block;
            margin: 4px 0 12px;
            color: #0878dc;
        }

        .review {
            display: block;
            background: #087bfa;
            color: white;
            padding: 14px;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
        }

        .review:hover { background: #0866d1; }

        @media (max-width: 850px) {
            .dealers { grid-template-columns: 1fr 1fr; }
        }

        @media (max-width: 560px) {
            .dealers { grid-template-columns: 1fr; }
            nav { align-items: flex-start; }
            nav a { margin-left: 0; margin-right: 15px; }
        }
    </style>
</head>

<body>
    <nav>
        <strong>Car Dealership</strong>
        <div>
            <a href="/">Home</a>
            <a href="/admin/">Cars</a>
            <a href="/static/About.html">About</a>
        </div>
        <div>
            <a href="/login/">Login</a>
            <a href="/register/">Register</a>
        </div>
    </nav>

    <section class="hero">
        <h1>Welcome to Car Dealership</h1>
        <p>Find the best cars from trusted dealers near you.</p>
    </section>

    <main>
        <h2>Our Dealers</h2>

        <div class="dealers">
            <article class="card">
                <div class="photo">Auto World</div>
                <h3>Auto World</h3>
                <p>123 Main Street</p>
                <p>Wichita, Kansas 67202</p>
                <p>316-555-0101</p>
                <a class="website" href="https://example.com">
                    Visit website
                </a>
                <a class="review" href="/dealer/1/">Review Dealer</a>
            </article>

            <article class="card">
                <div class="photo">City Motors</div>
                <h3>City Motors</h3>
                <p>456 Oak Avenue</p>
                <p>Topeka, Kansas 66603</p>
                <p>785-555-0102</p>
                <a class="website" href="https://example.com">
                    Visit website
                </a>
                <a class="review" href="/dealer/2/">Review Dealer</a>
            </article>

            <article class="card">
                <div class="photo">Premium Auto Group</div>
                <h3>Premium Auto Group</h3>
                <p>789 Pine Road</p>
                <p>Overland Park, Kansas 66204</p>
                <p>913-555-0103</p>
                <a class="website" href="https://example.com">
                    Visit website
                </a>
                <a class="review" href="/dealer/3/">Review Dealer</a>
            </article>
        </div>
    </main>
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