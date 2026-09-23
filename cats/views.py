from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    # Временно отключим пагинацию на уровне вьюсета, 
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year') 
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',) 
    ordering_fields = ('name', 'birth_year') 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer