from .models import Profile


def theme(request):

    if request.user.is_authenticated:

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        return {
            "current_theme": profile.theme
        }

    return {
        "current_theme": "default"
    }