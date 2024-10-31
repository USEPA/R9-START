import arcpy
import os, sys
from arcgis.gis import GIS
import smtplib, ssl
from datetime import datetime
print("Modules Imported: "+str(datetime.now().strftime("%m/%d/%Y %H:%M "))+(time.localtime().tm_zone))

### Variables section begin ###

# Set the path to the local project folder: (syntax: r"\\10.147.243.138\start\Removals\JHBaxter")
fldrPath = r"\\10.147.243.138\start\Removals\JHBaxter"
print('fldrPath: '+fldrPath)

# Concatenate folder path and project aprx name: (syntax:  os.path.join(fldrPath,"Baxter_Pro_2024.aprx"))
prjPath = os.path.join(fldrPath,"Baxter_Pro_2024.aprx")
print('prjPath: '+prjPath)

# Target service definition item name in AGOL: (syntax:  "JHBaxter_TCRA_TankStatus_15Min_Public")
sd_fs_name = "JHBaxter_TCRA_TankStatus_15Min_Public" #Usually same name as the map name in Pro
print('sd_fs_name: '+sd_fs_name)

# Target service definition item ID in AGOL:
sd_fs_ID = "5b93905640f9493ca733b0a3bdb876b2" #hosted feature layer is: ("4166f2106b424022a92a0ef21ec1e431")

# Relative path to local folder where the .sd and .sddraft files are located for the project:
sdPath = os.path.join(fldrPath, "Scripts\Overwrite_HostedService")
print('sdPath: '+sdPath)

#sddraft filename:
sddraft = os.path.join(sdPath, "JHBaxter_TCRA_TankStatus_15Min_Public.sddraft")
print('sddraft: '+sddraft)

#sd filename:
sd = os.path.join(sdPath, "JHBaxter_TCRA_TankStatus_15Min_Public.sd")
print('sd: '+sd)

# Path to metadata XML (not using on JH Baxter)
#sdMetaData = os.path.join(relPath, "metadata.xml")
#print(sdMetaData)

# Set AGOL sharing options
shrOrg = True   
shrEveryone = True
shrGroups = ("R10 JH Baxter Public Items")

### End variables section ###

### ArcGIS portal url and login ###
portal = GIS('pro')
token = portal._con.token
print("Logged in as: "+str(portal.properties.user.username))

def overwriteHostedServiceDef():
    logFile = open(sdPath+"\\LogFile.txt", "a")
    try:
        # Overwrite .sddraft and stage to SD
        print("Connecting to first layer in aprx map...")
        arcpy.env.overwriteOutput = True
        aprx = arcpy.mp.ArcGISProject(prjPath)
        mapName = aprx.listMaps(sd_fs_name)[0]
        lyr = mapName.listLayers()[0]
        print("Layer name: "+(str(lyr)))
        print("Creating SD file...")
        arcpy.mp.CreateWebLayerSDDraft(lyr, sddraft, sd_fs_name, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS','', True, True)
        arcpy.StageService_server(sddraft, sd)
        #arcpy.UploadServiceDefinition_server(sd, 'My Hosted Services')

        print("Connecting to {}".format(portal))

        # Find the SD in AGOL by item ID, overwrite, and set sharing and metadata
        print("Searching for original SD on portal...")
        sdItem = portal.content.get(sd_fs_ID)

        print("Found SD: {}, ID: {}".format(sdItem.title, sdItem.id))
        sdItem.update(data=sd) #metadata=sdMetaData)
        print("Overwriting existing feature service...")
        sdOverwrite = sdItem.publish(overwrite=True)

        if shrOrg or shrEveryone or shrGroups:
            print("Setting sharing options…")
            sdOverwrite.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

        print("Finished overwriting: {} – ID: {}".format(sdOverwrite.title, sdOverwrite.id))
        print("Overwritten at: "+str(datetime.now().strftime("%m/%d/%Y %H:%M "))+(time.localtime().tm_zone))
        logFile.write('\n'+"SUCCESSFUL overwrite at: "+str(datetime.now().strftime("%m/%d/%Y %H:%M "))+(time.localtime().tm_zone) \
                      +". Item: "+str(sdOverwrite.title)+". ID: "+str(sdOverwrite.id))
        logFile.close()
        
    except Exception as e:
        print("Process DID NOT run successfully. Updating log file...")
        print("Exception: "+ str(e))
        #msg = 'Scheduled task <Overwrite_GPhostedService_PublicStatus.py> did not run successfully. \n\n' + str(e)
        #send_Email(subject, msg, recipients)
        logFile.write('\n'+"FAILED overwrite at: "+str(datetime.now().strftime("%m/%d/%Y %H:%M "))+(time.localtime().tm_zone))
        logFile.close()
        
overwriteHostedServiceDef()
