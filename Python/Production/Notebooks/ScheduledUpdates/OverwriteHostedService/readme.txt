Setup for Overwriting Hosted Services script:

1) Workflow:  a scheduled task triggers a bat file that triggers the py file to overwrite hosted services

2) files needed in a project-specific subdirectory:
	- .bat file
	- .py file
	- .sd file (example SERVICE DEFINITION file not included for security reasons, create a placeholder .sd file for the project and it will be overwritten each run)
	- .sddraft file (example SERVICE DEFINITION DRAFT file not included for security reasons, create a placeholder .sddraft file for the project and it will be overwritten each run)
	- LogFile.txt (blank file for logging successful/failed runs if e-mail notifications disabled)

3) begin by doing development for project-specific variables in the .ipynb notebook file

4) when development for project-specific variables is completed in the notebook, copy text from all notebook cells into the .py file

5) revise the .bat file to target the correct filepaths:
	- filepath for the Pro environment python.exe file (normally a default arcgis location on C:\..., or specify another python instance - must have relevant packages that are called by the script installed if using non-Pro environment)
	- filepath for the project-specific .py file created above

6) create a scheduled task in Windows to run on desired timing (usually once nightly when overwriting public hosted services) that runs the .bat file

7) in this version of the script successful or failed runs will be print-appended to the LogFile.txt, alternatively admins can be e-mailed by the .py script if overwrite fails but this functionality not included in this version of script to protect server e-mail information