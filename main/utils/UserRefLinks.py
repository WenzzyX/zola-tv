from users.models import RefLink

def create_share_url(user, url):
    try:
        match = RefLink.objects.get(user=user, link=url)
        return False
    except RefLink.DoesNotExist:
        r_link = RefLink(
            user=user,
            link=url
        )
        r_link.save()
        return True

def click_ref_link(url):
    try:
        curr_link = RefLink.objects.get(link=url)
        curr_link.clicks += 1
        curr_link.save()
        return True
    except RefLink.DoesNotExist:
        return False

def add_download_to_url(url):
    try:
        curr_link = RefLink.objects.get(link=url)
        curr_link.downloads += 1
        curr_link.save()
        return True
    except RefLink.DoesNotExist:
        return False
