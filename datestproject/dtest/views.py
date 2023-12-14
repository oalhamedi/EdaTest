from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
import io
import markdown
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
from io import BytesIO
import base64
from ydata_profiling import ProfileReport

#global rows, columns, data, my_file, missing_values, mydict, dhead, dtail, dinfo, ddesc , dshap, dcor , graph, dheat, fig
# Create your views here.
def index(request):
    return render(request, 'index.html', {})

#def test(request):
#    return render(request, 'test.html', {})

def test(request):
    context = {}
    if request.method == "POST":
#        try:
           uploaded_file = request.FILES['document']
           print(uploaded_file)
           if uploaded_file.name.endswith('.csv'):
               # save file in media folder
               savefile = FileSystemStorage()
               name = savefile.save(uploaded_file.name, uploaded_file)  # name of the file
               # know where to save file
               d = os.getcwd()  # current directory of the project
               file_directory = d + '\media\\' + name
               readfile(file_directory)
               return redirect(results)
           elif uploaded_file.name.endswith('.xlsx'):
               # save file in media folder
               savefile = FileSystemStorage()
               name = savefile.save(uploaded_file.name, uploaded_file)  # name of the file
               # know where to save file
               d = os.getcwd()  # current directory of the project
               file_directory = d + '\media\\' + name
               read_file(file_directory)
               return redirect(results)
           elif uploaded_file.name.endswith('.xls'):
               # save file in media folder
               savefile = FileSystemStorage()
               name = savefile.save(uploaded_file.name, uploaded_file)  # name of the file
               # know where to save file
               d = os.getcwd()  # current directory of the project
               file_directory = d + '\media\\' + name
               read_file(file_directory)
               return redirect(results)
           else:
               messages.warning(request, 'File was not uploaded. Please use csv or xlsx file extension.')
#        except ValueError:
#            messages.error(request, "Please check data integrity!")

        #print(uploaded_file)


    return render(request, 'test.html', {})

#project.csv
def readfile(filename):
    global rows, columns, data, my_file, missing_values, mydict, dhead, dtail, dinfo, ddesc, dcor, graph, dheat

    my_file = pd.read_csv(filename, engine='python', index_col = False, sep='[: ; , | -]', error_bad_lines=False)
    data = pd.DataFrame(data=my_file)
    #my_file= read_file(filename)
   # data = pd.DataFrame(data=my_file)

    info = io.StringIO()
    data.info(buf=info)
    info.seek(0)

    ddesc = data.describe()

    dcor = data.corr()

    dheat = sns.heatmap(dcor, annot=False)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    graph = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    dhead = data.head(5)
    dtail = data.tail(5)

    mydict = {

        "dinfo": markdown.markdown(info.read()),
        "ddesc": ddesc.to_html(),
        "dcor":  dcor.to_html(),
        "dhead": dhead.to_html(),
        "dtail": dtail.to_html(),
        "chart": graph,

    }

    #rows and columns
    rows = len(data.axes[0])
    columns = len(data.axes[1])

    #find missing data
    missingsings = ['?','0','--']
    null_data = data[data.isnull().any(axis=1)]
    missing_values = len(null_data)

def read_file(filename):
    global rows, columns, data, my_file, missing_values, mydict, dhead, dtail, dinfo, ddesc, dcor, graph, dheat


    my_file = pd.read_excel(filename)
    data = pd.DataFrame(data=my_file)

        #    my_file = pd.read_excel(filename)
        #    data = pd.DataFrame(data=my_file)
        # my_file= read_file(filename)
        # data = pd.DataFrame(data=my_file)

    info = io.StringIO()
    data.info(buf=info)
    info.seek(0)

    ddesc = data.describe()

    dcor = data.corr()

    dheat = sns.heatmap(dcor, annot=False)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    graph = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    dhead = data.head(5)
    dtail = data.tail(5)

    mydict = {

            "dinfo": markdown.markdown(info.read()),
            "ddesc": ddesc.to_html(),
            "dcor": dcor.to_html(),
            "dhead": dhead.to_html(),
            "dtail": dtail.to_html(),
            "chart": graph,

    }

    # rows and columns
    rows = len(data.axes[0])
    columns = len(data.axes[1])

    # find missing data
    missingsings = ['?', '0', '--']
    null_data = data[data.isnull().any(axis=1)]
    missing_values = len(null_data)


def results(request):

    #try:

     message = 'I found ' +  str(rows) + ' rows and ' + str(columns) + ' columns. Missing data are: ' + str(missing_values)
     #message = info
     messages.warning(request, message)
     return render(request, 'results.html', context = mydict)
    #except ValueError:  # raised if `y` is empty.
    #    messages.error(request, "The file has the wrong format.")


def contact(request):
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        message = request.POST['message']

        data = {
            'name': message_name,
            'email': message_email,
            'message': message
        }
        message = '''
        New message: {}

        From: {}
        '''.format(data['message'], data['email'])

        # send an email
        send_mail(
            data['name'],  # subject
            message,  # message
            '',  # from email
            ['omardev81@gmail.com'],  # to email
            fail_silently=False,
        )

        return render(request, 'contact.html', {'message_name': message_name})
    else:
        return render(request, 'contact.html', {})

