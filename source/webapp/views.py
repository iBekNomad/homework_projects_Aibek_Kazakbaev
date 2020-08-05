from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView

from webapp.models import Issue
from .forms import IssueForm, BROWSER_DATETIME_FORMAT


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        if is_admin:
            data = Issue.objects.all()
        else:
            data = Issue.objects.filter(status='moderated')
        return render(request, 'index.html', context={
            'Issues': data
        })


class IssueView(TemplateView):
    template_name = 'Issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        Issue = get_object_or_404(Issue, pk=pk)

        context['Issue'] = Issue
        return context


class IssueCreateView(View):
    def get(self, request):
        form = IssueForm()
        return render(request, 'Issue_create.html', context={
            'form': form
        })

    def post(self, request):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            Issue = Issue.objects.create(**data)
            return redirect('Issue_view', pk=Issue.pk)
        else:
            return render(request, 'Issue_create.html', context={
                'form': form
            })


class IssueUpdateView(TemplateView):
    template_name = 'Issue_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        Issue = get_object_or_404(Issue, pk=pk)

        initial = {}
        for key in 'title', 'text', 'author', 'status':
            initial[key] = getattr(Issue, key)
        initial['publish_at'] = make_naive(Issue.publish_at).strftime(BROWSER_DATETIME_FORMAT)
        form = IssueForm(initial=initial)

        context['Issue'] = Issue
        context['form'] = form

        return context

    def post(self, request, pk):
        Issue = get_object_or_404(Issue, pk=pk)
        form = IssueForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(Issue, key, value)
            Issue.save()
            return redirect('Issue_view', pk=Issue.pk)
        else:
            return self.render_to_response({
                'Issue': Issue,
                'form': form
            })


def Issue_delete_view(request, pk):
    Issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'GET':
        return render(request, 'Issue_delete.html', context={'Issue': Issue})
    elif request.method == 'POST':
        Issue.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
