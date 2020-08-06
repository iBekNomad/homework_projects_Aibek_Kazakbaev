from django.db import models


class IssueType(models.Model):
    type = models.CharField(max_length=40, null=False, blank=False, verbose_name='Type')


class IssueStatus(models.Model):
    status = models.CharField(max_length=40, null=False, blank=False, verbose_name='Status')


class Issue(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Title')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Description')
    status = models.ForeignKey('webapp.IssueStatus', related_name='statuses', on_delete=models.PROTECT,
                               verbose_name='Status')
    type = models.ForeignKey('webapp.IssueType', related_name='types', on_delete=models.PROTECT, verbose_name='Type')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'
