from datetime import datetime as dt

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from dashboard.models import DataDocument



# class DataDocumentForm(ModelForm):
# 	class Meta:
# 		model = DataDocument
# 		fields = ['filename', 'title', 'url', 'product_category', 'data_group','matched','extracted']
# 	def __init__(self, *args, **kwargs):
# 		self.user = kwargs.pop('user', None)
# 		super(DataGroupForm, self).__init__(*args, **kwargs)
#
# # @login_required()
# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = DocumentForm()
#     return render(request, 'core/model_form_upload.html', {
#         'form': form
#     })

def register_upload(request, template='data_document/upload.html'):
    # num = str(DataDocument.objects.all().count()+1)
    print(request.session.keys())
    num = str(47)
    datagroup_pk = request.session['datagroup_pk']
    print(request.user.username)
    context = {'datagroup_pk': datagroup_pk,}
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fn = './doc/{}/{}_{}_{}'.format(request.session['datagroup_pk'],
                                        num,
                                        request.user.username,
                                        myfile.name)
        filename = fs.save(fn, myfile)
        uploaded_file_url = fs.url(filename)
        context['uploaded_file_url'] = uploaded_file_url
        # add to DD here
        return render(request, template, context)
    return render(request, template, context)
