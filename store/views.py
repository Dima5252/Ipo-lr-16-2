from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <h1>Главная страница</h1>

    <a href="/about/">Об авторе</a><br><br>

    <a href="/shop-info/">О магазине</a>
    """)


def about(request):
    return HttpResponse("""
    Автор работы: Дмитрий
    """)


def shop_info(request):
    return HttpResponse("""
    Интернет-магазин атрибутики из фильмов,
    сериалов, игр и мультфильмов.
    """)