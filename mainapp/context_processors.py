from mainapp.models import MenuItem


def menu(request):
    main_menu = MenuItem.objects.all()
    return {'menu': main_menu}
