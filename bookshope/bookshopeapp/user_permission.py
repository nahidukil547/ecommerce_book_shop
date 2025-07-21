from .models import UserPermission 

def checkUserPermission(request, access_type, menu_url):
    try:
        user_permission = {
            'can_add':"can_add",
            'can_view':"can_view",
            'can_update':"can_update",
            'can_delete':"can_delete",
        }
        if request.user.is_superuser :
            return True
        else:
            check_user_permission = UserPermission.objects.filter(
                user_id = request.user.id, 
                is_active= True,
                **{user_permission[access_type]:True},
                menu__menu_url = menu_url
            )
        if check_user_permission:
            return True
        else:
            return False
    except:
        return False