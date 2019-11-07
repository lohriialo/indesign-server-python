# What is Adobe InDesign Server?
Adobe InDesign Server is a scalable engine that let you programmatically create automated documents where the data is pulled from a variety of databases like a CMS/DAM etc. Use cases of InDesign Server are, generating documents to PDF, SVG, JPEG, EPS, XML etc. InDesign Server is used in a variety of content management workflows, print & publishing solutions.

# InDesign Server with Python
In this example, we'll demonstrate how you can use InDesign Server to publish with the data being pulled in from a [Firebase realtime database](https://firebase.google.com/).

#### Architecture #### 
![](https://i.imgur.com/w7LuamT.png "InDesign Server Python Publishing Architecture")

# Getting Started
Adobe InDesign Server is required to run this tutorial. InDesign Server has a 90 day  trial period, which should be enough to run a POC against your development environment.

# Install InDesign Server
* Download [here](https://www.adobeprerelease.com/beta/E31BC525-5F97-4E90-8ECD-5209CB404F08)

# Start InDesign Server
* `indesignserver -port 12345`

For more details, refer InDesign Server getting started guide at `<Install Dir>\Documentation\English\Intro to InDesign CC Server 2019.pdf`

# Setup
* `pip install flask`
* `pip install zeep`

# Example
```python
# Path to JSX script to do the export
exportScriptPath = "export_pdf.jsx"

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
```
# export_pdf.jsx
```javascript
function ExportAsPDF(myFile){  
    try{
       	app.documents.item(0).exportFile(ExportFormat.pdfType, myFile, app.pdfExportPresets.item("[High Quality Print]"));
    }catch(e){
    	alert(e);
    };  
}
function LoadDataIntoTemplate(doc){
	// using script label to place data into placeholders
	for (var idx = 0; idx < doc.allPageItems.length; idx++)
	{
		var pageItem = doc.allPageItems[idx];
		// Editorial contents
		if (pageItem.constructor.name == "TextFrame" && pageItem.label == "placeholder1")
		{
		  pageItem.contents = app.scriptArgs.getValue("arg1");
		}
		if (pageItem.constructor.name == "TextFrame" && pageItem.label == "placeholder2")
		{
		  pageItem.contents = app.scriptArgs.getValue("arg2");
		}
		if (pageItem.constructor.name == "TextFrame" && pageItem.label == "placeholder3")
		{
		  pageItem.contents = app.scriptArgs.getValue("arg3");
		}
	}
}
function main(){
	var myTemplateFile = new File("/c/ServerFiles/template.indt");
	var myPDFfile = new File("/c/ServerFiles/brochure.pdf");
	var doc = app.open(myTemplateFile);
	// get scriptArgs and update
	LoadDataIntoTemplate(doc);
	// Export as PDF
	ExportAsPDF(myPDFfile);
	doc.close();
	alert("PDF Exported");
}
main();
```

# Before
![](https://raw.githubusercontent.com/lohriialo/indesign-server-python/master/images/before-copy.jpg "Before")

# After
![](https://raw.githubusercontent.com/lohriialo/indesign-server-python/master/images/after.jpg "After")

# How to inspect a scripting object properties?
There's not a straight forward way, you need to read the documentation to understand what properties/attributes are available for a scripting object, or possibly a COM browser. For example, I've extracted the Python scripting object reference for InDesign CC 2018 at [doc_reference](https://github.com/lohriialo/indesign-server-python/tree/master/api_reference)

# InDesign Server Resources
* [InDesign Server Developer Forum](https://forums.adobe.com/community/indesign/indesign_server_developers)
* [InDesign Scripting Forum](https://forums.adobe.com/community/indesign/indesign_scripting)
