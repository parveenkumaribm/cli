# *****************************************************************************
# Copyright (c) 2024 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# *****************************************************************************

from os import path
from prompt_toolkit import print_formatted_text

class MongodbSettingsMixin():
    def configMongoDb(self) -> None:
         self.printH1("Configure MongoDb")
         self.printDescription([
            "The installer can setup mongoce in your OpenShift cluster (available only for amd64 )or you may choose to configure MAS to use an existing mongodb"
         ])

         if self.yesOrNo("Configure MongoDb in your OpenShift cluster"):
            self.promptForString("Install namespace", "mongodb_namespace", default="mongoce")
            self.setParam("mongodb_action", "install")
         else:
            mongodb_namespace = 'mongodb'
            self.setParam("mongodb_action", "byo")
            self.selectLocalConfigDir()

            instanceId = self.getParam('mas_instance_id')
            # Check if a configuration already exists before creating a new one
            mongoCfgFile = path.join(self.localConfigDir, f"mongo-{mongodb_namespace}.yaml")

            print_formatted_text(f"Searching for system mongodb configuration file in {mongoCfgFile} ...")
            if path.exists(mongoCfgFile):
                if self.yesOrNo(f"System mongodb configuration file 'mongo-{mongodb_namespace}.yaml' already exists.  Do you want to generate a new one"):
                    self.generateMongoCfg(instanceId=instanceId, destination=mongoCfgFile)
            else:
                print_formatted_text(f"Expected file ({mongoCfgFile}) was not found, generating a valid system mongodb configuration file now ...")
                self.generateMongoCfg(instanceId=instanceId,destination=mongoCfgFile)
