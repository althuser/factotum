import csv

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from dashboard.models import DataDocument, DataGroup



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

@login_required()
def register_upload(request, template='data_document/upload.html'):
    num = str(DataDocument.objects.all().count()+1)
    datagroup_pk = request.session['datagroup_pk']
    datagroup = DataGroup.objects.filter(pk=datagroup_pk)[0]
    context = {'datagroup_pk': datagroup_pk,}
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fn = './doc/{}/{}_{}_{}'.format(request.session['datagroup_pk'],
                                        num,
                                        request.user.username,
                                        myfile.name)
        filename = fs.save(fn, myfile)
        # add to DD here
        uploaded_file_url = fs.url(filename)
        context['uploaded_file_url'] = uploaded_file_url
        count = 0
        with open(uploaded_file_url) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['title']:
                    row['title'] = row['filename'].split('.')[0]
                doc = DataDocument(filename=row['filename'],
                                    title=row['title'],
                                    url=row['url'],
                                    product_category=row['product'],
                                    data_group=datagroup)
                doc.save()
                count += 1
                print(row['filename'],row['title'],row['product'],row['url'])
        context['uploaded_num'] = count
        return render(request, template, context)
    return render(request, template, context)
