from django.contrib import admin
from webapp.models import Issue, IssueType, IssueStatus


admin.site.register(Issue)
admin.site.register(IssueStatus)
admin.site.register(IssueType)
