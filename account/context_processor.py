def render_group(request):
    group = request.user.check_in_group()

    return {
        'account_group' : group
    }