# class WatchedVideosListAPIView(ListAPIView):
#     serializer_class = WatchedVideoSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return WatchedVideo.objects.filter(user=self.request.user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({
#             "results": serializer.data,
#             "total_results": len(serializer.data)
#         }, status=status.HTTP_200_OK)