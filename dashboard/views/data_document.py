import os
import csv
from collections import OrderedDict

# from settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from dashboard.models import DataDocument, DataGroup

@login_required()
def register_upload(request, template='data_document/upload.html'):
    datagroup_pk = request.session['datagroup_pk']
    datagroup = DataGroup.objects.filter(pk=datagroup_pk)[0]
    context = {'datagroup_pk': datagroup_pk,}
    if request.method == 'POST' and request.FILES['myfile']:
        user = request.user.username + '_'
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fn = './{}/{}'.format(datagroup, myfile.name)
        filename = fs.save(fn, myfile)
        uploaded_file_url = fs.url(filename)
        context['uploaded_file_url'] = uploaded_file_url
        print(os.path.join(os.getcwd(), uploaded_file_url))
        print(os.getcwd())
        with open(uploaded_file_url) as csvfile:
            reader = csv.DictReader(csvfile)
            up_num = len([i for i,d in enumerate(reader) if d['filename']])
            valid = up_num == reader.line_num-1
        if not valid: # missing filenames, delete and prompt to fix
            context['uploaded_file_url'] = 0
            context['fail'] = (reader.line_num-1) -up_num
            fs.delete(os.path.join(os.getcwd(), uploaded_file_url)) # problems here, test
            return render(request, template, context)
        # if not DataDocument.objects.last():
        #     start = 0
        # else:
        #     start = DataDocument.objects.last().pk
        new_f = '/'.join(uploaded_file_url.split('/')[:-1]+[user + myfile.name])
        ordered_fieldnames = OrderedDict([('DataDocument_id',None),
                                            ('filename',None),
                                            ('title',None),
                                            ('product',None),
                                            ('url',None)])
        with open(uploaded_file_url, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open(new_f, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=ordered_fieldnames,
                                        lineterminator='\n')
                writer.writeheader()
                for row in reader:
                    print(row['filename'])
                    if not row['title']:
                        row['title'] = row['filename'].split('.')[0]
                    doc = DataDocument(filename=row['filename'],
                                        title=row['title'],
                                        url=row['url'],
                                        product_category=row['product'],
                                        data_group=datagroup)
                    doc.save()
                    row['DataDocument_id'] = doc.id
                    writer.writerow(row)
        fs.delete(os.path.join(os.getcwd(), uploaded_file_url))
        context['uploaded_num'] = up_num
        return render(request, template, context)
    return render(request, template, context)
