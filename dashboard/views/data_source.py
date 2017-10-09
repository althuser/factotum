from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from dashboard.views import *
from dashboard.models import DataSource
from datetime import datetime

class DataSourceForm(ModelForm):
	class Meta:
		model = DataSource
		fields = ['title', 'url', 'type', 'description']


def data_source_list(request, template_name='data_source/datasource_list.html'):
	datasource = DataSource.objects.all()
	data = {}
	data['object_list'] = datasource
	return render(request, template_name, data)


def data_source_detail(request, pk, template_name='data_source/datasource_detail.html'):
	datasource = get_object_or_404(DataSource, pk=pk)
	return render(request, template_name, {'object': datasource})


def data_source_create(request, template_name='data_source/datasource_form.html'):
	form = DataSourceForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('data_source_list')
	return render(request, template_name, {'form': form})


def data_source_update(request, pk, template_name='data_source/datasource_form.html'):
	datasource = get_object_or_404(DataSource, pk=pk)
	form = DataSourceForm(request.POST or None, instance=datasource)
	if form.is_valid():
		datasource.updated_at = datetime.now()
		form.save()
		return redirect('data_source_list')
	return render(request, template_name, {'form': form})


def data_source_delete(request, pk, template_name='data_source/datasource_confirm_delete.html'):
	datasource = get_object_or_404(DataSource, pk=pk)
	if request.method == 'POST':
		datasource.delete()
		return redirect('data_source_list')
	return render(request, template_name, {'object': datasource})