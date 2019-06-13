from flask import Flask, render_template, flash, redirect, url_for
from zeep import Client
import os

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/exportPDF')
def exportPDF():

    # InDesign JSX script to do the export
    exportScriptPath = os.getcwd() + "\export_pdf.jsx"
    # soap client = IDS host client running on a soap port
    client = Client('http://localhost:12345?wsdl')

    # Create SOAP call params object, based on IDS wsdl
    # For details go to http://localhost:12345?wsdl
    RunScriptParameters = client.get_type('ns0:RunScriptParameters')
    IDSP_ScriptArg = client.get_type('ns0:IDSP-ScriptArg')

    # Get editorial contents from database
    # this example returns a dictionary{} of editorial data
    editorialContents = {'arg1': 'Electric Cars',
                         'arg2': 'An electric car is an automobile that is propelled by one or more electric motors, using energy stored in rechargeable batteries.',
                         'arg3': 'The first practical electric cars were produced in the 1880s'}

    # pass the data to RunScript so you can access them from your .jsx file like so: app.scriptArgs.getValue("frontTitle");
    params = RunScriptParameters("", "javascript", exportScriptPath, [IDSP_ScriptArg(key, value) for key, value in editorialContents.items()])

    result = client.service.RunScript(params)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('localhost', 8001, debug=True,)

