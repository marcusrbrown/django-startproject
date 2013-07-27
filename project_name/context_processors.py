"""Request processors used locally."""

# TODO: Move these into a reusable library.


def analytical_domain(request):
    """
    Adds the analytical_domain context variable to the context (used by
    django-analytical).
    """
    return {'analytical_domain': request.get_host()}
