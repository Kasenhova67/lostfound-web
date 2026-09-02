from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from lost.models import itemlost, itemfound
from users.models import Profile
from .serializers import ItemLostSerializer, ItemFoundSerializer, ProfileSerializer

class ItemLostListCreateView(generics.ListCreateAPIView):
    queryset = itemlost.objects.all().order_by('-date', '-time')
    serializer_class = ItemLostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_title', 'place', 'description']
    ordering_fields = ['date', 'time']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(username=self.request.user.username)
        else:
            serializer.save(username='Anonymous')

class ItemLostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = itemlost.objects.all()
    serializer_class = ItemLostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(username=self.request.user.username)

class ItemFoundListCreateView(generics.ListCreateAPIView):
    queryset = itemfound.objects.all().order_by('-date', '-time')
    serializer_class = ItemFoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_title', 'place', 'description']
    ordering_fields = ['date', 'time']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(username=self.request.user.username)
        else:
            serializer.save(username='Anonymous')

class ItemFoundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = itemfound.objects.all()
    serializer_class = ItemFoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class SearchView(generics.ListAPIView):
    serializer_class = ItemLostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return itemlost.objects.filter(
                Q(product_title__icontains=query) |
                Q(place__icontains=query) |
                Q(description__icontains=query)
            )
        return itemlost.objects.none()
