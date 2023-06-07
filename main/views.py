from django.shortcuts import render
from .utils import DataMixin
from .models import Product, Order
from django.views.generic import ListView, View, CreateView
from .forms import CategoryFilterForm
from django.contrib import messages

# Create your views here.
class Home(DataMixin, View):
    model = Product
    template_name = 'index.html'
    context_object_name = 'product', 'cart_quantity',

    def get_queryset(self):
        return self.model.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        cart = self.cart(request)
        cart_quantity = self.cart_quantity(cart)
        context = {
            self.context_object_name[0]: products,
            'cart_quantity': cart_quantity,
        }

        return render(request, self.template_name, context)


class Catalogue(DataMixin, View):
    form_class = CategoryFilterForm
    model = Product
    template_name = 'catalogue.html'
    success_url = '/catalogue/'

    def get_queryset(self):
        return self.model.objects.all()

    def form_valid(self, form):
        categories = form.cleaned_data['categories']
        return categories

    def form_invalid(self, form):
        return messages.error("Invalid form")

    def get(self, request, *args, **kwargs):
        cart = self.cart(request)
        cart_quantity = self.cart_quantity(cart)
        products = self.model.objects.all()
        form = self.form_class(request.GET or None)
        if request.GET and form.is_valid():
            categories = self.form_valid(form)
            products = products.filter(type__in=categories)
        quantity_of_diff_products = products.count()
        context = {
            'products': products,
            'category_filter_form': form,
            'cart_quantity': cart_quantity,
            'count': quantity_of_diff_products
        }
        return render(request, self.template_name, context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


def logout_view(request):
    logout(request)
    return redirect('home')

