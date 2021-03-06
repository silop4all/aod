

(function (globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function (n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  
  /* gettext library */

  django.catalog = {
    " - select <br/> a non registered email": "- \u03b5\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5 <br/>\u03ad\u03bd\u03b1 \u03bc\u03b7 \u03ba\u03b1\u03c4\u03b1\u03c7\u03c9\u03c1\u03b7\u03bc\u03ad\u03bd\u03bf email", 
    " and select unique username": "\u03ba\u03b1\u03b9 \u03b5\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5 \u03bc\u03bf\u03bd\u03b1\u03b4\u03b9\u03ba\u03cc \u03cc\u03bd\u03bf\u03bc\u03b1 \u03c7\u03c1\u03ae\u03c3\u03c4\u03b7", 
    " to setup his/her network of assistance services on behalf of him/her.\nYour request has been submitted.": "\u03b3\u03b9\u03b1 \u03c4\u03b7\u03bd \u03b5\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03c4\u03bf\u03c5/\u03c4\u03b7\u03c2 \u03b4\u03b9\u03ba\u03c4\u03cd\u03bf\u03c5 \u03ba\u03b1\u03b8\u03bf\u03b4\u03b7\u03b3\u03bf\u03cd\u03bc\u03b5\u03bd\u03c9\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03b5\u03ba \u03bc\u03ad\u03c1\u03bf\u03c5\u03c2 \u03c4\u03bf\u03c5 / \u03c4\u03b7\u03c2. \n\u03a4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03ac \u03c3\u03b1\u03c2 \u03ad\u03c7\u03b5\u03b9 \u03c5\u03c0\u03bf\u03b2\u03bb\u03b7\u03b8\u03b5\u03af.", 
    " without the network removal": "\u03c7\u03c9\u03c1\u03af\u03c2 \u03c4\u03b7\u03bd \u03b1\u03c6\u03b1\u03af\u03c1\u03b5\u03c3\u03b7 \u03c4\u03bf\u03c5 \u03b4\u03b9\u03ba\u03c4\u03cd\u03bf\u03c5", 
    "% Complete (success)": "% \u039f\u03bb\u03bf\u03ba\u03bb\u03ae\u03c1\u03c9\u03c3\u03b7 (\u03b5\u03c0\u03b9\u03c4\u03c5\u03c7\u03ce\u03c2)", 
    "'": "'", 
    "Accepted": "\u0391\u03c0\u03bf\u03b4\u03b5\u03ba\u03c4\u03cc", 
    "Access the service configuration\n that provider suggests": "\u0394\u03b5\u03af\u03c4\u03b5 \u03c4\u03b7 \u03b4\u03b9\u03b1\u03bc\u03cc\u03c1\u03c6\u03c9\u03c3\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03c0\u03bf\u03c5 \u03c0\u03c1\u03bf\u03c4\u03b5\u03af\u03bd\u03b5\u03b9 \u03bf \u03c0\u03ac\u03c1\u03bf\u03c7\u03bf\u03c2 ", 
    "Add": "\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7", 
    "All languages are supported": "\u03a5\u03c0\u03bf\u03c3\u03c4\u03b7\u03c1\u03af\u03b6\u03bf\u03bd\u03c4\u03b1\u03b9 \u03cc\u03bb\u03b5\u03c2 \u03bf\u03b9 \u03b3\u03bb\u03ce\u03c3\u03c3\u03b5\u03c2", 
    "An error has occurred. The service modification failed": "\u0397 \u03b5\u03bd\u03b7\u03bc\u03ad\u03c1\u03c9\u03c3\u03b7 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5 \u03bb\u03cc\u03b3\u03c9 \u03b5\u03bd\u03cc\u03c2 \u03c3\u03c6\u03ac\u03bb\u03bc\u03b1\u03c4\u03bf\u03c2", 
    "An error is occured. The service modification failed": "\u0397 \u03b5\u03bd\u03b7\u03bc\u03ad\u03c1\u03c9\u03c3\u03b7 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5. \u03a0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03c4\u03b5 \u03be\u03ac\u03bd\u03b1", 
    "An error occured": "\u0388\u03bd\u03b1 \u03c3\u03c6\u03ac\u03bb\u03bc\u03b1 \u03c3\u03c5\u03bd\u03ad\u03b2\u03b7", 
    "An error occurred an your request has been abandoned.": "\u0388\u03bd\u03b1 \u03bb\u03ac\u03b8\u03bf\u03c2 \u03c0\u03c1\u03bf\u03ad\u03b9\u03c5\u03c8\u03b5 \u03ba\u03b1\u03b9 \u03c4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03ac \u03c3\u03b1\u03c2 \u03b5\u03b3\u03ba\u03b1\u03c4\u03b1\u03bb\u03b5\u03af\u03c6\u03b8\u03b7\u03ba\u03b5", 
    "AoD message": "\u039c\u03ae\u03bd\u03c5\u03bc\u03b1 \u03b1\u03c0\u03cc AoD", 
    "AoD scans the services that meet your requirements": "\u0397 AOD \u03c3\u03b1\u03c1\u03ce\u03bd\u03b5\u03b9 \u03c4\u03b9\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c0\u03bf\u03c5 \u03b1\u03bd\u03c4\u03b1\u03c0\u03bf\u03ba\u03c1\u03af\u03bd\u03bf\u03bd\u03c4\u03b1\u03b9 \u03c3\u03c4\u03b9\u03c2 \u03b1\u03c0\u03b1\u03b9\u03c4\u03ae\u03c3\u03b5\u03b9\u03c2 \u03c3\u03b1\u03c2", 
    "Cancel assistance request": "\u0391\u03ba\u03cd\u03c1\u03c9\u03c3\u03b7 \u03b1\u03b9\u03c4\u03ae\u03bc\u03b1\u03c4\u03bf\u03c2 \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2", 
    "Cancel your assistance on": "\u0391\u03ba\u03cd\u03c1\u03c9\u03c3\u03b7 \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2", 
    "Charging policy": "\u03a0\u03bf\u03bb\u03b9\u03c4\u03b9\u03ba\u03ae \u03c7\u03c1\u03ad\u03c9\u03c3\u03b7\u03c2", 
    "Confirm": "\u0395\u03c0\u03b9\u03b2\u03b5\u03b2\u03b1\u03af\u03c9\u03c3\u03b7", 
    "Constraints": "\u03a0\u03b5\u03c1\u03b9\u03bf\u03c1\u03b9\u03c3\u03bc\u03bf\u03af", 
    "Contact information was updated!": "\u039f\u03b9 \u03c0\u03bb\u03b7\u03c1\u03bf\u03c6\u03bf\u03c1\u03af\u03b5\u03c2 \u03b5\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03af\u03b5\u03c2 \u03b5\u03bd\u03b7\u03bc\u03b5\u03c1\u03ce\u03b8\u03b7\u03ba\u03b1\u03bd", 
    "Continue": "\u03a3\u03c5\u03bd\u03ad\u03c7\u03b5\u03b9\u03b1", 
    "Continue!": "\u03a3\u03c5\u03bd\u03ad\u03c7\u03b5\u03b9\u03b1!", 
    "Customize the service configuration": "\u03a0\u03c1\u03bf\u03c3\u03b1\u03c1\u03bc\u03cc\u03c3\u03c4\u03b5 \u03c4\u03b7 \u03c1\u03cd\u03b8\u03bc\u03b9\u03c3\u03b7 \u03c0\u03b1\u03c1\u03b1\u03bc\u03ad\u03c4\u03c1\u03c9\u03bd \u03c4\u03c9\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd", 
    "Debug state: ": "\u039a\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03b5\u03ba\u03c3\u03c6\u03b1\u03bb\u03bc\u03ac\u03c4\u03c9\u03c3\u03b7\u03c2", 
    "Denote service as interesting": "\u0394\u03b7\u03bb\u03ce\u03c3\u03c4\u03b5 \u03c4\u03b7\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1 \u03c9\u03c2 \u03b5\u03bd\u03b4\u03b9\u03b1\u03c6\u03ad\u03c1\u03bf\u03c5\u03c3\u03b1", 
    "Edit the service": "\u0395\u03c0\u03b5\u03be\u03b5\u03c1\u03b3\u03b1\u03c3\u03af\u03b1 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2", 
    "Error": "\u03a3\u03c6\u03ac\u03bb\u03bc\u03b1", 
    "Error in services' retrieval": "\u03a3\u03c6\u03ac\u03bb\u03bc\u03b1 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7\u03bd \u03b1\u03bd\u03ac\u03ba\u03c4\u03b7\u03c3\u03b7 \u03c4\u03c9\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd", 
    "Express your interest": "\u0395\u03ba\u03b4\u03ae\u03bb\u03c9\u03c3\u03b7 \u03b5\u03bd\u03b4\u03b9\u03b1\u03c6\u03ad\u03c1\u03bf\u03bd\u03c4\u03bf\u03c2", 
    "FREE": "\u0394\u03a9\u03a1\u0395\u0391\u039d", 
    "Fail in registration": "\u0397 \u03b5\u03b3\u03b3\u03c1\u03b1\u03c6\u03ae \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5", 
    "First button:": "\u03a0\u03c1\u03ce\u03c4\u03bf \u03ba\u03bf\u03c5\u03bc\u03c0\u03af:", 
    "Forbidden": "\u0391\u03c0\u03b1\u03b3\u03bf\u03c1\u03ad\u03c5\u03b5\u03c4\u03b1\u03b9", 
    "Get stats": "\u039b\u03ae\u03c8\u03b7 \u03c3\u03c4\u03b1\u03c4\u03b9\u03c3\u03c4\u03b9\u03ba\u03ce\u03bd", 
    "Human-based": "\u0391\u03bd\u03b8\u03c1\u03ce\u03c0\u03b9\u03bd\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2", 
    "ID": "\u03a4\u03b1\u03c5\u03c4\u03cc\u03c4\u03b7\u03c4\u03b1", 
    "Image file": "\u0391\u03c1\u03c7\u03b5\u03af\u03bf \u03b5\u03b9\u03ba\u03cc\u03bd\u03b1\u03c2", 
    "In case you cancel your assistance to a person with disabilities, the selected and purchased services will not be removed.": "\u03a3\u03b5 \u03c0\u03b5\u03c1\u03af\u03c0\u03c4\u03c9\u03c3\u03b7 \u03c0\u03bf\u03c5 \u03b1\u03ba\u03c5\u03c1\u03ce\u03c3\u03b5\u03c4\u03b5 \u03c4\u03b7\u03bd \u03c3\u03c5\u03bd\u03b4\u03c1\u03bf\u03bc\u03ae \u03c3\u03b1\u03c2 \u03c3\u03b5 \u03ad\u03bd\u03b1 \u03ac\u03c4\u03bf\u03bc\u03bf \u03bc\u03b5 \u03b1\u03bd\u03b1\u03c0\u03b7\u03c1\u03af\u03b1, \u03bf\u03b9 \u03b5\u03c0\u03b9\u03bb\u03b5\u03b3\u03bc\u03ad\u03bd\u03b5\u03c2 \u03ba\u03b1\u03b9 \u03b1\u03b3\u03bf\u03c1\u03b1\u03c3\u03bc\u03ad\u03bd\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03b4\u03b5\u03bd \u03b8\u03b1 \u03b1\u03c6\u03b1\u03b9\u03c1\u03b5\u03b8\u03bf\u03cd\u03bd.", 
    "Initiate properties of buttons": "\u0391\u03c1\u03c7\u03b9\u03ba\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03b9\u03b4\u03b9\u03bf\u03c4\u03ae\u03c4\u03c9\u03bd \u03ba\u03bf\u03c5\u03bc\u03c0\u03b9\u03ce\u03bd", 
    "Installation guidelines": "\u039f\u03b4\u03b7\u03b3\u03af\u03b5\u03c2 \u03b5\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7\u03c2", 
    "Invalid email": "\u039c\u03b7 \u03ad\u03b3\u03ba\u03c5\u03c1\u03bf email", 
    "Invalid input": "\u039c\u03b7 \u03ad\u03b3\u03ba\u03c5\u03c1\u03b7 \u03b5\u03af\u03c3\u03bf\u03b4\u03bf\u03c2", 
    "Languages": "\u0393\u03bb\u03ce\u03c3\u03c3\u03b5\u03c2", 
    "Latitude": "\u0393\u03b5\u03c9\u03b3\u03c1\u03b1\u03c6\u03b9\u03ba\u03cc \u03c0\u03bb\u03ac\u03c4\u03bf\u03c2", 
    "Longitude": "\u0393\u03b5\u03c9\u03b3\u03c1\u03b1\u03c6\u03b9\u03ba\u03cc \u03bc\u03ae\u03ba\u03bf\u03c2", 
    "Machine-based": "\u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03bb\u03bf\u03b3\u03b9\u03c3\u03bc\u03b9\u03ba\u03bf\u03cd", 
    "More details": "\u039b\u03b5\u03c0\u03c4\u03bf\u03bc\u03ad\u03c1\u03b5\u03b9\u03b5\u03c2", 
    "NO": "\u039f\u03a7\u0399", 
    "Network of assistance services": "\u0394\u03af\u03ba\u03c4\u03c5\u03bf \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03b2\u03bf\u03ae\u03b8\u03b5\u03b9\u03b1\u03c2", 
    "Network of assistance services ": "\u0394\u03af\u03ba\u03c4\u03c5\u03bf \u03ba\u03b1\u03b8\u03bf\u03b4\u03b7\u03b3\u03bf\u03cd\u03bc\u03b5\u03bd\u03c9\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd", 
    "Network of assistance services: installation steps": "\u0394\u03af\u03ba\u03c4\u03c5\u03bf \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03b2\u03bf\u03ae\u03b8\u03b5\u03b9\u03b1\u03c2: \u03b2\u03ae\u03bc\u03b1\u03c4\u03b1 \u03b5\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7\u03c2", 
    "Network of carers": "\u0394\u03af\u03ba\u03c4\u03c5\u03bf \u03c5\u03c0\u03bf\u03c3\u03c4\u03b7\u03c1\u03b9\u03ba\u03c4\u03ce\u03bd", 
    "No configuration has been set by service provider!": "\u0394\u03b5\u03bd \u03ad\u03c7\u03b5\u03b9 \u03bf\u03c1\u03b9\u03c3\u03c4\u03b5\u03af \u03c1\u03cd\u03b8\u03bc\u03b9\u03c3\u03b7 \u03b1\u03c0\u03cc \u03c4\u03bf\u03bd \u03c0\u03ac\u03c1\u03bf\u03c7\u03bf \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2!", 
    "No services selected. Navigate in the previous steps to select some services": "\u0394\u03b5\u03bd \u03ad\u03c7\u03bf\u03c5\u03bd \u03b5\u03c0\u03b9\u03bb\u03b5\u03c7\u03b8\u03b5\u03af \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2. \u03a0\u03b5\u03c1\u03b9\u03b7\u03b3\u03b7\u03b8\u03b5\u03af\u03c4\u03b5 \u03c3\u03c4\u03b1 \u03c0\u03c1\u03bf\u03b7\u03b3\u03bf\u03cd\u03bc\u03b5\u03bd\u03b1 \u03b2\u03ae\u03bc\u03b1\u03c4\u03b1 \u03b3\u03b9\u03b1 \u03bd\u03b1 \u03b5\u03c0\u03b9\u03bb\u03ad\u03be\u03b5\u03c4\u03b5 \u03ba\u03ac\u03c0\u03bf\u03b9\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2", 
    "No user feedback.": "\u0394\u03b5\u03bd \u03c5\u03c0\u03ac\u03c1\u03c7\u03bf\u03c5\u03bd \u03c3\u03c7\u03cc\u03bb\u03b9\u03b1 \u03b1\u03c0\u03cc \u03c4\u03bf \u03c7\u03c1\u03ae\u03c3\u03c4\u03b7", 
    "No, I do not agree!": "\u038c\u03c7\u03b9, \u03b4\u03b5 \u03c3\u03c5\u03bc\u03c6\u03c9\u03bd\u03ce!", 
    "Not available": "\u039c\u03b7 \u03b4\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03bf\u03c2", 
    "Office Excel dociument": "\u0388\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf \u03c4\u03bf\u03c5 Office Excel", 
    "Office Excel document": "\u0388\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf \u03c4\u03bf\u03c5 Office Excel", 
    "Office word document": "\u0388\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf \u03c4\u03bf\u03c5 Office Word", 
    "Oops, an error is occured!!!": "\u0388\u03bd\u03b1 \u03c3\u03c6\u03ac\u03bb\u03bc\u03b1 \u03c0\u03c1\u03bf\u03ad\u03ba\u03c5\u03c8\u03b5!", 
    "Parameters": "\u03a0\u03b1\u03c1\u03ac\u03bc\u03b5\u03c4\u03c1\u03bf\u03b9", 
    "Pdf document": "\u0388\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf Pdf", 
    "Pending": "\u0395\u03ba\u03ba\u03c1\u03b5\u03bc\u03b5\u03af", 
    "Platform settings were updated!": "\u039f\u03b9 \u03c1\u03c5\u03b8\u03bc\u03af\u03c3\u03b5\u03b9\u03c2 \u03c4\u03b7\u03c2 \u03b5\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ae\u03c2 \u03ad\u03c7\u03bf\u03c5\u03bd \u03b5\u03bd\u03b7\u03bc\u03b5\u03c1\u03c9\u03b8\u03b5\u03af!", 
    "Price": "\u039a\u03cc\u03c3\u03c4\u03bf\u03c2", 
    "Proceed to service purchase": "\u03a3\u03c5\u03bd\u03b5\u03c7\u03af\u03c3\u03c4\u03b5 \u03c3\u03c4\u03b7\u03bd \u03b1\u03b3\u03bf\u03c1\u03ac \u03c4\u03b7\u03c2 \u03c5\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2", 
    "Purchase": "\u0391\u03b3\u03bf\u03c1\u03ac", 
    "Purchased": "\u0391\u03b3\u03bf\u03c1\u03b1\u03c3\u03bc\u03ad\u03bd\u03b7", 
    "Remove": "\u0391\u03c6\u03b1\u03af\u03c1\u03b5\u03c3\u03b7", 
    "Remove an insteresting service": "\u0391\u03c6\u03b1\u03af\u03c1\u03b5\u03c3\u03b7 \u03b6\u03b7\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2", 
    "Remove the service": "\u0391\u03c6\u03b1\u03b9\u03c1\u03ad\u03c3\u03c4\u03b5 \u03c4\u03b7\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1", 
    "Requirements": "\u03a0\u03c1\u03bf\u03b1\u03c0\u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd", 
    "Search progress": "\u03a0\u03c1\u03cc\u03bf\u03b4\u03bf\u03c2 \u03b1\u03bd\u03b1\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7\u03c2", 
    "Second button:": "\u0394\u03b5\u03cd\u03c4\u03b5\u03c1\u03bf \u03ba\u03bf\u03c5\u03bc\u03c0\u03af:", 
    "Select service": "\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1", 
    "Service": "\u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1", 
    "Service configuration that provider offers": "\u03a1\u03cd\u03b8\u03bc\u03b9\u03c3\u03b7 \u03c0\u03b1\u03c1\u03b1\u03bc\u03ad\u03c4\u03c1\u03c9\u03bd \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03c0\u03bf\u03c5 \u03c0\u03c1\u03bf\u03c3\u03c6\u03ad\u03c1\u03b5\u03c4\u03b1\u03b9 \u03b1\u03cc \u03c4\u03bf\u03bd \u03c0\u03ac\u03c1\u03bf\u03c7\u03bf", 
    "Service logo": "\u039b\u03bf\u03b3\u03cc\u03c4\u03c5\u03c0\u03bf \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2", 
    "Service owner does not provide further documents (pdf, office documents, images, etc..)": "\u039f \u03b9\u03b4\u03b9\u03bf\u03ba\u03c4\u03ae\u03c4\u03b7\u03c2 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b4\u03b5\u03bd \u03c0\u03b1\u03c1\u03ad\u03c7\u03b5\u03b9 \u03b5\u03c0\u03b9\u03c0\u03bb\u03ad\u03bf\u03bd \u03ad\u03b3\u03b3\u03c1\u03b1\u03c6\u03b1 (pdf, office, \u03b5\u03b9\u03ba\u03cc\u03bd\u03b5\u03c2 \u03ba\u03c4\u03bb)", 
    "Service owner does not provide videos": "\u039f \u03b9\u03b4\u03b9\u03bf\u03ba\u03c4\u03ae\u03c4\u03b7\u03c2 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b4\u03b5\u03bd \u03c0\u03b1\u03c1\u03ad\u03c7\u03b5\u03b9 \u03bf\u03c0\u03c4\u03b9\u03ba\u03bf\u03b1\u03ba\u03bf\u03c5\u03c3\u03c4\u03b9\u03ba\u03cc \u03c5\u03bb\u03b9\u03ba\u03cc", 
    "Set up the network of assistance services of": "\u03a1\u03cd\u03b8\u03bc\u03b9\u03c3\u03b7 \u03c4\u03bf\u03c5 \u03b4\u03b9\u03ba\u03c4\u03cd\u03bf\u03c5 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2 \u03b3\u03b9\u03b1", 
    "Show statistics": "\u0394\u03b5\u03af\u03be\u03b5 \u03c3\u03c4\u03b1\u03c4\u03b9\u03c3\u03c4\u03b9\u03ba\u03ac", 
    "Sorry, an error has occurred": "\u039b\u03c5\u03c0\u03bf\u03cd\u03bc\u03b1\u03c3\u03c4\u03b5, \u03c0\u03b1\u03c1\u03bf\u03c5\u03c3\u03b9\u03ac\u03c3\u03c4\u03b7\u03ba\u03b5 \u03ad\u03bd\u03b1 \u03c3\u03c6\u03ac\u03bb\u03bc\u03b1", 
    "Sorry, try again!": "\u039b\u03c5\u03c0\u03bf\u03cd\u03bc\u03b1\u03c3\u03c4\u03b5, \u03c0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03c4\u03b5 \u03be\u03b1\u03bd\u03ac!", 
    "Start": "\u0391\u03c1\u03c7\u03ae", 
    "Success registration": "\u0397 \u03b5\u03b3\u03b3\u03c1\u03b1\u03c6\u03ae \u03bf\u03bb\u03bf\u03ba\u03bb\u03b7\u03c1\u03ce\u03b8\u03b7\u03ba\u03b5 \u03b5\u03c0\u03b9\u03c4\u03c5\u03c7\u03ce\u03c2", 
    "Swap properties of buttons": "\u0395\u03bd\u03b1\u03bb\u03bb\u03b1\u03b3\u03ae \u03b9\u03b4\u03b9\u03bf\u03c4\u03ae\u03c4\u03c9\u03bd \u03c4\u03c9\u03bd \u03ba\u03bf\u03c5\u03bc\u03c0\u03b9\u03ce\u03bd", 
    "The AoD platform wants your permission to track your location. Do you agree with this action?": "\u0397 \u03c0\u03bb\u03b1\u03c4\u03c6\u03cc\u03c1\u03bc\u03b1 AOD \u03b8\u03ad\u03bb\u03b5\u03b9 \u03c4\u03b7\u03bd \u03ac\u03b4\u03b5\u03b9\u03ac \u03c3\u03b1\u03c2 \u03b3\u03b9\u03b1 \u03bd\u03b1 \u03c0\u03b1\u03c1\u03b1\u03ba\u03bf\u03bb\u03bf\u03c5\u03b8\u03b5\u03af \u03c4\u03b7 \u03b8\u03ad\u03c3\u03b7 \u03c3\u03b1\u03c2. \u03a3\u03c5\u03bc\u03c6\u03c9\u03bd\u03b5\u03af\u03c4\u03b5 \u03bc\u03b5 \u03b1\u03c5\u03c4\u03ae \u03c4\u03b7\u03bd \u03b5\u03bd\u03ad\u03c1\u03b3\u03b5\u03b9\u03b1;", 
    "The deletion of this service failed": "\u0397 \u03b4\u03b9\u03b1\u03b3\u03c1\u03b1\u03c6\u03ae \u03b1\u03c5\u03c4\u03ae\u03c2 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5.", 
    "The distance value must be a non negative number. Keep in mind that this value maps to kilometers.": "\u0397 \u03c4\u03b9\u03bc\u03ae \u03c4\u03b7\u03c2 \u03b1\u03c0\u03cc\u03c3\u03c4\u03b1\u03c3\u03b7\u03c2 \u03b4\u03b5\u03bd \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03ad\u03bd\u03b1\u03c2 \u03b1\u03c1\u03bd\u03b7\u03c4\u03b9\u03ba\u03cc\u03c2 \u03b1\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2. \u039b\u03ac\u03b2\u03b5\u03c4\u03b5 \u03c5\u03c0\u03cc\u03c8\u03b7 \u03cc\u03c4\u03b9 \u03b7 \u03c4\u03b9\u03bc\u03ae \u03b1\u03c5\u03c4\u03ae \u03b1\u03bd\u03c4\u03b9\u03c3\u03c4\u03bf\u03b9\u03c7\u03af\u03b6\u03b5\u03c4\u03b1\u03b9 \u03c3\u03b5 \u03c7\u03b9\u03bb\u03b9\u03cc\u03bc\u03b5\u03c4\u03c1\u03b1.", 
    "The maximum price value must be greater than (or equal with) the minimum one!": "\u0397 \u03bc\u03ad\u03b3\u03b9\u03c3\u03c4\u03b7 \u03c4\u03b9\u03bc\u03ae \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03bc\u03b5\u03b3\u03b1\u03bb\u03cd\u03c4\u03b5\u03c1\u03b7 \u03b1\u03c0\u03cc (\u03ae \u03af\u03c3\u03b7 \u03bc\u03b5) \u03c4\u03bf \u03b5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03bf \u03ad\u03bd\u03b1!", 
    "The maximum value of Quality of Service field is out of range. Please enter a value in range [0,5]!": "\u0397 \u03bc\u03ad\u03b3\u03b9\u03c3\u03c4\u03b7 \u03c4\u03b9\u03bc\u03ae \u03c4\u03bf\u03c5 \u03c0\u03b5\u03b4\u03af\u03bf\u03c5 \u03a0\u03bf\u03b9\u03cc\u03c4\u03b7\u03c4\u03b1 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03b5\u03ba\u03c4\u03cc\u03c2 \u03c4\u03bf\u03c5 \u03b5\u03c0\u03b9\u03c4\u03c1\u03b5\u03c0\u03c4\u03bf\u03cd. \u03a0\u03b1\u03c1\u03b1\u03ba\u03b1\u03bb\u03ce \u03b5\u03b9\u03c3\u03ac\u03b3\u03b5\u03c4\u03b5 \u03bc\u03b9\u03b1 \u03c4\u03b9\u03bc\u03ae \u03c3\u03c4\u03bf \u03b4\u03b9\u03ac\u03c3\u03c4\u03b7\u03bc\u03b1 [0,5]!", 
    "The maximum value of Quality of Service field must be greater than (or equal with) the corresponding minimum one!": "\u0397 \u03bc\u03ad\u03b3\u03b9\u03c3\u03c4\u03b7 \u03c4\u03b9\u03bc\u03ae \u03c4\u03bf\u03c5 \u03c0\u03b5\u03b4\u03af\u03bf\u03c5 \u03a0\u03bf\u03b9\u03cc\u03c4\u03b7\u03c4\u03b1 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03bc\u03b5\u03b3\u03b1\u03bb\u03cd\u03c4\u03b5\u03c1\u03b7 \u03b1\u03c0\u03cc (\u03ae \u03af\u03c3\u03b7 \u03bc\u03b5) \u03c4\u03bf \u03b1\u03bd\u03c4\u03af\u03c3\u03c4\u03bf\u03b9\u03c7\u03bf \u03b5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03bf \u03ad\u03bd\u03b1!", 
    "The minimum value of Quality of Service field is out of range. Please enter a value in range [0,5]!": "\u0397 \u03b5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03b7 \u03c4\u03b9\u03bc\u03ae \u03c4\u03bf\u03c5 \u03c0\u03b5\u03b4\u03af\u03bf\u03c5 \u03a0\u03bf\u03b9\u03cc\u03c4\u03b7\u03c4\u03b1 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03b9\u03ce\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03b5\u03ba\u03c4\u03cc\u03c2 \u03c4\u03bf\u03c5 \u03b5\u03c0\u03b9\u03c4\u03c1\u03b5\u03c0\u03c4\u03bf\u03cd. \u03a0\u03b1\u03c1\u03b1\u03ba\u03b1\u03bb\u03ce \u03b5\u03b9\u03c3\u03ac\u03b3\u03b5\u03c4\u03b5 \u03bc\u03b9\u03b1 \u03c4\u03b9\u03bc\u03ae \u03c3\u03c4\u03bf \u03b4\u03b9\u03ac\u03c3\u03c4\u03b7\u03bc\u03b1 [0,5]!", 
    "The price values must be non negative numbers!": "\u039f\u03b9 \u03c4\u03b9\u03bc\u03ad\u03c2 \u03b4\u03b5\u03bd \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03b1\u03c1\u03bd\u03b7\u03c4\u03b9\u03ba\u03cc\u03c2 \u03b1\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2!", 
    "The replace of the cover image failed. Try again": "\u0397 \u03b1\u03bb\u03bb\u03b1\u03b3\u03ae \u03c4\u03bf\u03c5 \u03b5\u03be\u03ce\u03c6\u03c5\u03bb\u03bb\u03bf\u03c5 \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5. \u03a0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03c4\u03b5 \u03c0\u03ac\u03bb\u03b9", 
    "The replace of the logo failed. Try again": "\u0397 \u03b1\u03bb\u03bb\u03b1\u03b3\u03ae \u03c4\u03bf\u03c5 \u03b5\u03b9\u03ba\u03cc\u03bd\u03b1\u03c2 \u03b1\u03c0\u03ad\u03c4\u03c5\u03c7\u03b5. \u03a0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03c4\u03b5 \u03c0\u03ac\u03bb\u03b9", 
    "The response in this request is still pending": "\u0397 \u03b1\u03c0\u03ac\u03bd\u03c4\u03b7\u03c3\u03b7 \u03c3\u03b5 \u03b1\u03c5\u03c4\u03cc \u03c4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03b5\u03ba\u03ba\u03c1\u03b5\u03bc\u03b5\u03af", 
    "The service searching was aborted.": "\u0397 \u03b1\u03bd\u03b1\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03bc\u03b1\u03c4\u03b1\u03b9\u03ce\u03b8\u03b7\u03ba\u03b5.", 
    "The service title is ": "\u039f \u03c4\u03af\u03c4\u03bb\u03bf\u03c2 \u03c4\u03b7\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03b5\u03af\u03bd\u03b1\u03b9", 
    "This service has been purchased": "\u0397 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1 \u03ad\u03c7\u03b5\u03b9 \u03b1\u03b3\u03bf\u03c1\u03b1\u03c3\u03c4\u03b5\u03af", 
    "Try again!": "\u03a0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03c4\u03b5 \u03be\u03b1\u03bd\u03ac!", 
    "Type": "\u0395\u03af\u03b4\u03bf\u03c2", 
    "Type a non registered email": "\u0395\u03b9\u03c3\u03ac\u03b3\u03b5\u03c4\u03b5 \u03ad\u03bd\u03b1 \u03bc\u03b7 \u03ba\u03b1\u03c4\u03b1\u03c7\u03c9\u03c1\u03b7\u03bc\u03ad\u03bd\u03bf email", 
    "Type a non registered username": "\u0395\u03b9\u03c3\u03ac\u03b3\u03b5\u03c4\u03b5 \u03ad\u03bd\u03b1 \u03bc\u03b7 \u03ba\u03b1\u03c4\u03b1\u03c7\u03c9\u03c1\u03b7\u03bc\u03ad\u03bd\u03bf \u03cc\u03bd\u03bf\u03bc\u03b1 \u03c7\u03c1\u03ae\u03c3\u03c4\u03b7", 
    "Type at least 4 characters<br>without spaces": "\u03a0\u03bb\u03b7\u03ba\u03c4\u03c1\u03bf\u03bb\u03bf\u03b3\u03ae\u03c3\u03c4\u03b5 \u03c4\u03bf\u03c5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03bf\u03bd 4 \u03c7\u03b1\u03c1\u03b1\u03ba\u03c4\u03ae\u03c1\u03b5\u03c2 <br> \u03c7\u03c9\u03c1\u03af\u03c2 \u03ba\u03b5\u03bd\u03ac", 
    "Unit": "\u039d\u03cc\u03bc\u03b9\u03c3\u03bc\u03b1", 
    "Useful link": "\u03a7\u03c1\u03ae\u03c3\u03b9\u03bc\u03bf\u03c2 \u03a3\u03cd\u03bd\u03b4\u03b5\u03c3\u03bc\u03bf\u03c2", 
    "User feedback for the service": "\u03a3\u03c7\u03cc\u03bb\u03b9\u03b1 \u03c7\u03c1\u03ae\u03c3\u03c4\u03b7 \u03b3\u03b9\u03b1 \u03c4\u03b7\u03bd \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1", 
    "Values": "\u03a4\u03b9\u03bc\u03ad\u03c2", 
    "Video presentation": "\u03a0\u03b1\u03c1\u03bf\u03c5\u03c3\u03af\u03b1\u03c3\u03b7 \u03b2\u03af\u03bd\u03c4\u03b5\u03bf", 
    "View": "\u0398\u03ad\u03b1", 
    "View on the map": "\u0394\u03b5\u03af\u03c4\u03b5 \u03c3\u03c4\u03bf\u03bd \u03c7\u03ac\u03c1\u03c4\u03b7", 
    "YES": "\u039d\u0391\u0399", 
    "Yes, I agree!": "\u039d\u03b1\u03b9, \u03c3\u03c5\u03bc\u03c6\u03c9\u03bd\u03ce!", 
    "You have not selected services for all categories. If you want to declare more services as interesting or purchase more, please click on Select service button of the corresponding category.": "\u0394\u03b5\u03bd \u03ad\u03c7\u03b5\u03c4\u03b5 \u03b5\u03c0\u03b9\u03bb\u03ad\u03be\u03b5\u03b9 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03b3\u03b9\u03b1 \u03cc\u03bb\u03b5\u03c2 \u03c4\u03b9\u03c2 \u03ba\u03b1\u03c4\u03b7\u03b3\u03bf\u03c1\u03af\u03b5\u03c2. \u0391\u03bd \u03b8\u03ad\u03bb\u03b5\u03c4\u03b5 \u03bd\u03b1 \u03b4\u03b7\u03bb\u03ce\u03c3\u03b5\u03c4\u03b5 \u03c0\u03b5\u03c1\u03b9\u03c3\u03c3\u03cc\u03c4\u03b5\u03c1\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c9\u03c2 \u03b5\u03bd\u03b4\u03b9\u03b1\u03c6\u03ad\u03c1\u03bf\u03c5\u03c3\u03b5\u03c2 \u03ae \u03bd\u03b1 \u03b1\u03b3\u03bf\u03c1\u03ac\u03c3\u03b5\u03c4\u03b5 \u03c0\u03b5\u03c1\u03b9\u03c3\u03c3\u03cc\u03c4\u03b5\u03c1\u03b5\u03c2, \u03c0\u03b1\u03c1\u03b1\u03ba\u03b1\u03bb\u03bf\u03cd\u03bc\u03b5 \u03ba\u03ac\u03bd\u03c4\u03b5 \u03ba\u03bb\u03b9\u03ba \u03c3\u03c4\u03bf \u03ba\u03bf\u03c5\u03bc\u03c0\u03af \u0395\u03c0\u03b9\u03bb\u03bf\u03b3\u03ae \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2 \u03c4\u03b7\u03c2 \u03b1\u03bd\u03c4\u03af\u03c3\u03c4\u03bf\u03b9\u03c7\u03b7\u03c2 \u03ba\u03b1\u03c4\u03b7\u03b3\u03bf\u03c1\u03af\u03b1\u03c2.", 
    "You need permission from ": "\u03a7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c3\u03c4\u03b5 \u03ac\u03b4\u03b5\u03b9\u03b1 \u03b1\u03c0\u03cc", 
    "Your assistance request has accepted": "\u03a4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03ae\u03c2 \u03c3\u03b1\u03c2 \u03ad\u03c7\u03b5\u03b9 \u03b3\u03af\u03bd\u03b5\u03b9 \u03b1\u03c0\u03bf\u03b4\u03b5\u03ba\u03c4\u03cc", 
    "Your assistance request has rejected": "\u03a4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03ae\u03c2 \u03c3\u03b1\u03c2 \u03b4\u03b5\u03bd \u03ad\u03c7\u03b5\u03b9 \u03b3\u03af\u03bd\u03b5\u03b9 \u03b1\u03c0\u03bf\u03b4\u03b5\u03ba\u03c4\u03cc", 
    "Your assistance request is still pending": "\u03a4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03ae\u03c2 \u03c3\u03b1\u03c2 \u03b5\u03ba\u03ba\u03c1\u03b5\u03bc\u03b5\u03af", 
    "Your browser does not support the video tag.": "\u03a4\u03bf \u03c0\u03c1\u03cc\u03b3\u03c1\u03b1\u03bc\u03bc\u03b1 \u03c0\u03b5\u03c1\u03b9\u03ae\u03b3\u03b7\u03c3\u03ae\u03c2 \u03c3\u03b1\u03c2 \u03b4\u03b5\u03bd \u03c5\u03c0\u03bf\u03c3\u03c4\u03b7\u03c1\u03af\u03b6\u03b5\u03b9 \u03c4\u03b7\u03bd \u03b5\u03c4\u03b9\u03ba\u03ad\u03c4\u03b1 \u03b2\u03af\u03bd\u03c4\u03b5\u03bf.", 
    "Your invitation has been sent on ": "\u0397 \u03c0\u03c1\u03cc\u03c3\u03ba\u03bb\u03b7\u03c3\u03ae \u03c3\u03b1\u03c2 \u03ad\u03c7\u03b5\u03b9 \u03b1\u03c0\u03bf\u03c3\u03c4\u03b1\u03bb\u03b5\u03af", 
    "error": "\u039b\u03ac\u03b8\u03bf\u03c2", 
    "error 2": "\u03c3\u03c6\u03ac\u03bb\u03bc\u03b1-2", 
    "load service details error": "\u039b\u03ac\u03b8\u03bf\u03c2 \u03c3\u03c4\u03b7 \u03c6\u03cc\u03c1\u03c4\u03c9\u03c3\u03b7 \u03c4\u03c9\u03bd \u03bb\u03b5\u03c0\u03c4\u03bf\u03bc\u03b5\u03c1\u03b5\u03b9\u03ce\u03bd \u03c4\u03b7\u03c2 \u03c5\u03b7\u03c1\u03b5\u03c3\u03af\u03b1\u03c2"
  };

  django.gettext = function (msgid) {
    var value = django.catalog[msgid];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return (typeof(value) == 'string') ? value : value[0];
    }
  };

  django.ngettext = function (singular, plural, count) {
    var value = django.catalog[singular];
    if (typeof(value) == 'undefined') {
      return (count == 1) ? singular : plural;
    } else {
      return value[django.pluralidx(count)];
    }
  };

  django.gettext_noop = function (msgid) { return msgid; };

  django.pgettext = function (context, msgid) {
    var value = django.gettext(context + '\x04' + msgid);
    if (value.indexOf('\x04') != -1) {
      value = msgid;
    }
    return value;
  };

  django.npgettext = function (context, singular, plural, count) {
    var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
    if (value.indexOf('\x04') != -1) {
      value = django.ngettext(singular, plural, count);
    }
    return value;
  };
  

  django.interpolate = function (fmt, obj, named) {
    if (named) {
      return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
    } else {
      return fmt.replace(/%s/g, function(match){return String(obj.shift())});
    }
  };


  /* formatting library */

  django.formats = {
    "DATETIME_FORMAT": "d/m/Y P", 
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S", 
      "%d/%m/%Y %H:%M:%S.%f", 
      "%d/%m/%Y %H:%M", 
      "%d/%m/%Y", 
      "%d/%m/%y %H:%M:%S", 
      "%d/%m/%y %H:%M:%S.%f", 
      "%d/%m/%y %H:%M", 
      "%d/%m/%y", 
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d"
    ], 
    "DATE_FORMAT": "d/m/Y", 
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y", 
      "%d/%m/%y", 
      "%Y-%m-%d"
    ], 
    "DECIMAL_SEPARATOR": ",", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "j F", 
    "NUMBER_GROUPING": "3", 
    "SHORT_DATETIME_FORMAT": "d/m/Y P", 
    "SHORT_DATE_FORMAT": "d/m/Y", 
    "THOUSAND_SEPARATOR": "\u00a0", 
    "TIME_FORMAT": "P", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
  };

  django.get_format = function (format_type) {
    var value = django.formats[format_type];
    if (typeof(value) == 'undefined') {
      return format_type;
    } else {
      return value;
    }
  };

  /* add to global namespace */
  globals.pluralidx = django.pluralidx;
  globals.gettext = django.gettext;
  globals.ngettext = django.ngettext;
  globals.gettext_noop = django.gettext_noop;
  globals.pgettext = django.pgettext;
  globals.npgettext = django.npgettext;
  globals.interpolate = django.interpolate;
  globals.get_format = django.get_format;

}(this));

