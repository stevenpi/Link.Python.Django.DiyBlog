from django.utils.text import slugify


def get_slug(slug_string, model):
    slug = slugify(slug_string)
    same_slugs_count = model.objects.filter(slug__icontains=slug).count()
    if 0 < same_slugs_count:
        # whitespace to let slugify create a hyphen
        slug += "-" + str(same_slugs_count)
    return slug
