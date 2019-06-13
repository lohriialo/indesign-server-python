# What is Adobe InDesign Server?
Adobe InDesign Server is a scalable engine that let you programmatically create automated documents where the data is pulled from a variety of databases like a CMS/DAM etc. Use cases of InDesign Server are, generating documents to PDF, SVG, JPEG, EPS, XML etc. InDesign Server is used in a variety of content management workflows, print & publishing solutions.

# InDesign Server with Python
In this example, we'll demonstrate how you can use InDesign Server to publish with the data being pulled in from a Firbase database.

#### Architecture #### 
![](https://i.imgur.com/w7LuamT.png "Photoshop Python")

# Getting Started
Adobe InDesign Server is required to run this tutorial. InDesign Server has a 90 day  trial period, which should be enough to run a POC against your development environment.

# Install & start InDesign Server
* Download [here](https://www.adobeprerelease.com/beta/E31BC525-5F97-4E90-8ECD-5209CB404F08)
* `indesignserver -port 12345`

For more details, refer InDesign Server getting started guide at `<Install Dir>\Documentation\English\Intro to InDesign CC Server 2019.pdf`

# Setup
* `pip install flask`
* `pip install zeep`

# Example
```python
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

    # Path to JSX script to do the export
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
```

# Before
![](https://raw.githubusercontent.com/lohriialo/indesign-server-python/master/images/before.jpg "Before")

# After
![](https://raw.githubusercontent.com/lohriialo/indesign-server-python/master/images/after.jpg "After")
