from rest_framework.permissions import BasePermission , SAFE_METHODS


class isOwnerOrReadOnly_Profile(BasePermission):
    def has_object_permission(self, request, view, obj):
        #permission to allow only the owner of profile to update otherwise read only
        if request.method in SAFE_METHODS:
            return True
        
        return request.user == obj.user
    


class isOwnerOrReadOnly_Post(BasePermission):
    def has_object_permission(self, request, view, obj):
        #permission to allow only the owner of profile to update otherwise read only
        if request.method in SAFE_METHODS:
            return True
        
        return request.user == obj.author