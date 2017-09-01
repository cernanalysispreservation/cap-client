API
======

.. _types:

Retrieve current user information
----------

.. code-block:: console

	$ cap-client me

	{
        "collaborations": [
        "ATLAS",
        "LHCb",
        "CMS",
        "ALICE"
    ],
    "id": 1,
    "email": "user@cern.ch",
    }





Get all types of analyses available
----------

.. code-block:: console

	$ cap-client types

	Available types:
		atlas-workflows
		alice-analysis
		atlas-analysis
		lhcb
		cms-questionnaire
		cms-analysis


Get analysis with given PID
----------

You can get existing analyses details only if you have at least read access to it.

You need to specify 
 
	--pid  the PID of an analysis.

.. code-block:: console

	$ cap-client get --pid/-p <existing pid>

	E.g $ cap-client get --pid 883090d3c1784aeabe9e23412a81239e

	{   
		"pid": "883090d3c1784aeabe9e23412a81239e",
	    "basic_info": {
	        "abstract": "Example abstract",
	        "people_info": [
	            {
	                "name": "John doe"
	            },
	            {
	                "name": "J doe"
	            }
	        ],
	        "analysis_number": "test"
	    }
	}


Create analysis
----------

You can create a new analysis by specifing

	--file  a file with the json data corresponding to the analysis JSON Schema.
	--type  the type of analysis you want to create.

If you don't know what is the type of analyses you want to create use this 
:ref:`link <types>`.

You can only choose to create the type of analysis that you are affiliated.
E.g if you are a CMS member you can only create analysis with type cms-analysis or 
cms-questionnaire.


.. code-block:: console

	$ cap-client create --file/-f <file with JSON data>  --type/-t <type of analysis> 

	E.g $ cap-client create --file test.json --type cms-analysis

	{
		'status': 200, 
		'data': {   
			"pid": "883090d3c1784aeabe9e23412a81239e",
		    "basic_info": {
		        "abstract": "Example abstract",
		        "people_info": [
		            {
		                "name": "John doe"
		            },
		            {
		                "name": "J doe"
		            }
		        ],
		        "analysis_number": "test"
		    }
		}
	}
		


Delete analysis
----------

You can delete an existing analysis by specifing

	--pid  the PID as a parameter.

	.. code-block:: console

		$ cap-client delete --pid/-p <existing pid>

		E.g $ cap-client delete --pid 4c734c3ae5b14a2195e3b17dc9ff63ae

		Server response:
			{
				'status': 204, 
			 	'data': None
			}


Update analysis
----------

You can update an existing analysis by specifing

	--pid  the PID as a parameter.
	--file  a file with the json data corresponding to the analysis JSON Schema.


	.. code-block:: console

		$ cap-client update --pid/-p <existing pid> --file/-f <file with JSON data>

		E.g $ cap-client update --pid 883090d3c1784aeabe9e23412a81239e --file test.json

		{
		 	'status': 200, 
		 	'data': {   
				"pid": "883090d3c1784aeabe9e23412a81239e",
			    "basic_info": {
			        "abstract": "Example abstract",
			        "people_info": [
			            {
			                "name": "John doe"
			            },
			            {
			                "name": "J doe"
			            }
			        ],
			        "analysis_number": "test"
			    }
			}
		}

Patch analysis
----------

You can patch an existing analysis by specifing

	--pid  the PID as a parameter.
	--file  a file with the changes in `JSON patch format <http://jsonpatch.com/>`_.

Example changes in JSON patch format:

	.. code-block:: javascript
		[ { "op": "add", "path": "/basic_info/analysis_number", "value": "22" }]

.. code-block:: console

	$ cap-client patch --pid/-p <existing pid> --file/-f <file with JSON data>

	E.g $ cap-client patch --pid 883090d3c1784aeabe9e23412a81239e --file test.json
	
	{
	 	'status': 200, 
	 	'data': {   
			"pid": "883090d3c1784aeabe9e23412a81239e",
		    "basic_info": {
		        "abstract": "Example abstract",
		        "people_info": [
		            {
		                "name": "John doe"
		            },
		            {
		                "name": "J doe"
		            }
		        ],
		        "analysis_number": "test"
		    }
		}
	}


Metadata
--------
You can get existing analyses metadata only if you have at least read access to it.

You need to specify

	--pid  the PID of an analysis.

.. code-block:: console

    $ cap-client metadata get --pid/-p <existing pid>

    E.g $ cap-client metadata get --pid 4b2924db6c32467bb2de6221f4faf167

    {
        "$ana_type": "lhcb",
        "$schema": "https://macbook-trzcinska.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json",
    }


