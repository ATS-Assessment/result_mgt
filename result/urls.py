from django.urls import path

from .views import index, UpdateResultView, AllResultView,\
    ResultDetailView

urlpatterns = [
    # path('', index, name='index'),
    # path('create/', CreateResultView.as_view(), name='result_create'),
    # path('all-results/', AllResultView.as_view(), name='result-list'),
    # path('all-results/<int:pk>/', ResultDetailView.as_view(), name='result_detail'),
    # # path('all-results/<int:pk>/delete/', delete_result_view, name='result_delete'),
    # path('all-results/<int:pk>/update/',
    #      UpdateResultView.as_view(), name='result_update'),

]
