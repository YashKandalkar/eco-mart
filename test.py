import json
t = {
    "VCAP_SERVICES": {
        "dashDB": [
            {
                "binding_guid": "30b9504c-a428-44eb-b750-8f01c84347e4",
                "binding_name": "null",
                "credentials": {
                    "apikey": "TbJCllsptdJra2otw9v6LijSa9gXcdY9UO3zb0msplue",
                    "db": "BLUDB",
                    "host": "db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com",
                    "hostname": "db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com",
                    "https_url": "https://db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com",
                    "iam_apikey_description": "Auto-generated for binding 97015a4f-453a-4582-bae8-01011d54a711",
                    "iam_apikey_name": "sqldatabase",
                    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                    "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/b426663ba26b4be9b667dfea9f854343::serviceid:ServiceId-d63a5554-0a51-4359-aec9-95711e63cfba",
                    "parameters": {
                        "role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                        "serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/b426663ba26b4be9b667dfea9f854343::serviceid:ServiceId-d63a5554-0a51-4359-aec9-95711e63cfba"
                    },
                    "password": "8FxMb34HHWOVAzhzKs8kL15@_MTi4",
                    "port": 50001,
                    "ssldsn": "DATABASE=BLUDB;HOSTNAME=db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com;PORT=50001;PROTOCOL=TCPIP;UID=bluadmin;PWD=8FxMb34HHWOVAzhzKs8kL15@_MTi4;Security=SSL;",
                    "ssljdbcurl": "jdbc:db2://db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com:50001/BLUDB:sslConnection=true;",
                    "uri": "db2://bluadmin:8FxMb34HHWOVAzhzKs8kL15%40_MTi4@db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com:50001/BLUDB?ssl=true;",
                    "username": "bluadmin"
                },
                "instance_guid": "45ecdcf2-0b27-4b13-b81c-f16e80054d5a",
                "instance_name": "sqldatabase",
                "label": "dashDB",
                "name": "sqldatabase",
                "plan": "Flex One",
                "provider": "null",
                "syslog_drain_url": "null",
                "tags": [
                    "big_data",
                    "ibm_created",
                    "ibm_dedicated_public",
                    "db2",
                    "sqldb",
                    "purescale",
                    "apidocs_enabled",
                    "sql",
                    "dashdb",
                    "dash",
                    "database",
                    "analytics",
                    "flex",
                    "dbaas",
                    "smp",
                    "mpp",
                    "ibmcloud-alias"
                ],
                "volume_mounts": []
            }
        ]
    }
}

tt = {"VCAP_APPLICATION": {
    "application_id": "23c42e0e-e30c-4cfa-bf4a-de0cb1303186",
    "application_name": "lastAttempt",
    "application_uris": [
      "lastAttempt.eu-gb.cf.appdomain.cloud"
      ],
    "application_version": "7cf194eb-b349-4132-ada9-2e4251479eab",
    "cf_api": "https://api.eu-gb.cf.cloud.ibm.com",
    "limits": {
        "disk": 1024,
        "fds": 16384,
        "mem": 256
    },
    "name": "lastAttempt",
    "organization_id": "8d9a96e8-f8d6-4270-8984-59ebed7962e7",
    "organization_name": "neha1304.v@gmail.com",
    "process_id": "23c42e0e-e30c-4cfa-bf4a-de0cb1303186",
    "process_type": "web",
    "space_id": "cb958a4a-8713-422e-a305-cee6ac6d52be",
    "space_name": "dev",
    "uris": [
        "lastAttempt.eu-gb.cf.appdomain.cloud"
    ],
    "users": "null",
    "version": "7cf194eb-b349-4132-ada9-2e4251479eab"
}}

with open('.env', 'w') as f:
    json.dump(t, f)
    f.write("\n")
    s = json.dumps(tt)
    f.write(s)
