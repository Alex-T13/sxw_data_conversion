from django.http import HttpResponseRedirect
from django.shortcuts import render

# Imaginary function to handle an uploaded file.
from applications.upload.forms import AddMaterialsForm
from apps import handle_uploaded_file


def upload_file(request):
    if request.method == 'POST':
        form = AddMaterialsForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = AddMaterialsForm()
    return render(request, 'upload.html', {'form': form})