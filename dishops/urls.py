from django.contrib.admin import register
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    CookExperienceUpdateView,
    CookDeleteView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    CookListView,
    CookDetailView,
    CookCreateView,
    UserLoginView,
    logout_view,
    UserPasswordResetConfirmView,
    UserPasswordResetView,
    UserPasswordChangeView,
    IndexView,
    ToggleAssignToDishView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "dish_types/",
        DishTypeListView.as_view(),
        name="dish_type_list",
    ),
    path(
        "dish_types/create/",
        DishTypeCreateView.as_view(),
        name="dish_type_create",
    ),
    path(
        "dish_types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish_type_update",
    ),
    path(
        "dish_types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish_type_delete",
    ),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path(
        "dishes/<int:pk>/update/",
        DishUpdateView.as_view(),
        name="dish-update"
    ),
    path(
        "dishes/<int:pk>/delete/",
        DishDeleteView.as_view(),
        name="dish-delete"
    ),
    path(
        "dish/<int:pk>/toggle-assign/",
        ToggleAssignToDishView.as_view(),
        name="toggle-assign-to-dish"
    ),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path(
        "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path(
        "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),

    path(
        "cooks/<int:pk>/update/",
        CookExperienceUpdateView.as_view(),
        name="cook-update",
    ),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete"
    ),


    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    path(
        'accounts/password-change/',
        UserPasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'accounts/password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'accounts/password-reset/',
        UserPasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'accounts/password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'accounts/password-reset-confirm/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'accounts/password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

app_name = "dishops"
