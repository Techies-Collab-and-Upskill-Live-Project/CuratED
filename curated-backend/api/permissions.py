from rest_framework import permissions

class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsVideoWatcher(permissions.BasePermission):
    """
    Custom permission to only allow users who have watched a video to comment/rate it
    """
    def has_permission(self, request, view):
        video_id = request.data.get('video_id') or view.kwargs.get('video_id')
        if not video_id:
            return False
        return request.user.watchedvideo_set.filter(video_id=video_id).exists()
