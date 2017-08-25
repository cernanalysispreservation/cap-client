Usage
=====

This guide assumes that you have successfully installed cap-client package already. If not, please follow the  :doc:`installation` instructions first.

To use cap-client you need a running CAP server, you can use the `CERN Production server <https://analysispreservation.cern.ch/>`_.  

Next step is to generate an access token through the CAP server. For CERN Production server this can be done by following this `link <https://analysispreservation.cern.ch/profile/applications>`_.

Finally you need to set the required environment variables for the cap-client.

.. code-block:: console

	$ export CAP_SERVER_URL=https://analysispreservation.cern.ch/
	$ export CAP_ACCESS_TOKEN=<your generated access token from server>

Note that CAP_ACCESS_TOKEN can also be passed as an argument in the command line interface.
