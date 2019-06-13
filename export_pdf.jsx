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
	var myFile = new File("/c/ServerFiles/brochure.pdf");
	var doc = app.open(myTemplateFile);

	// get scriptArgs and update
	LoadDataIntoTemplate(doc);

	// Export as PDF
	ExportAsPDF(myFile);

	doc.close();
	alert("PDF Exported");
}

main();