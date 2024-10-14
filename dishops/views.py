from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from dishops.models import Cook, Dish, DishType
from dishops.forms import (
    DishTypeSearchForm,
    DishSearchForm,
    DishForm,
    CookExperienceUpdateForm,
    CookCreationForm,
    CookSearchForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm,
)

print(UserPasswordResetForm)



@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "dishops/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "dishops/dish_type_list.html"
    paginate_by = 5

    queryset = DishType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return self.queryset.filter(name__icontains=name)
        return self.queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("dishops:dish_type_list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("dishops:dish_type_list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("dishops:dish_type_list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "dishops/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.select_related("dish_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        dish_type = self.request.GET.get("dish_type", "")
        context["search_form"] = DishSearchForm(initial={"dish_type": dish_type})
        return context

    def get_queryset(self):
        dish_type = self.request.GET.get("dish_type")
        if dish_type:
            return self.queryset.filter(dish_type__name__icontains=dish_type)
        return self.queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "dishops/dish_detail.html"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("dishops:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("dishops:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("dishops:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    queryset = Cook.objects.all()
    template_name = "dishops/cook_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")

        if username:
            return self.queryset.filter(username__icontains=username)
        return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "dishops/cook_detail.html"
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    template_name = "dishops/cook_form.html"
    form_class = CookCreationForm


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = AuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('/accounts/login')


class CookExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("dishops:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("dishops:cook-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)

    if (
        Dish.objects.get(id=pk) in cook.dishes.all()
    ):  # probably could check if dish exists
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("dishops:dish-detail", args=[pk]))


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
