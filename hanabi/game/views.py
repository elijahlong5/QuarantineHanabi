from django.shortcuts import render

# from django.http import HttpResponse
# from django.template import loader


def main(request):
    print()
    return render(request, "game/main.html")
    # return HttpResponse(
    #     loader.get_template("templates/main.html").render({}, request)
    # )
