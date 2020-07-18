from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from courses.models import Courses
from category.models import Category, Subcategory


# Create your views here.
class CategoryListView(ListView):
    model = Courses
    template_name = 'category/category_view.html'
    context_object_name = 'category_context'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Courses.objects.filter(category=category)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        context['title'] = 'Category'
        return context


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'category/subcategory_view.html'
    context_object_name = 'subcategory_context'

    def get_queryset(self):
        subcategory = get_object_or_404(Subcategory, slug=self.kwargs['slug'])
        return Subcategory.objects.filter(subcategory=subcategory)

    def get_context_data(self, *args, **kwargs):
        context = super(SubcategoryListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Learning Path'
        context['course_list'] = Courses.objects.all()
        return context
