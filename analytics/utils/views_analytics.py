from main.models import Movie, Serie, Show, Sport, Channel


def clear_views(model):
    try:
        objects = model.objects.all()
        for el in objects:
            el.watch_counter = 0
            el.save()
    except:
        return False
    return True


def clear_all_views():
    clear_views(Movie)
    clear_views(Serie)
    clear_views(Show)
    clear_views(Sport)
    clear_views(Channel)