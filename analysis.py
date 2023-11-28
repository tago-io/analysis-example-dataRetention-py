"""
Analysis Example
Custom Data Retention

Get the list of devices, then go to each device removing the
variables you chooses.
"""
from tagoio_sdk import Analysis, Device, Resources


# The function myAnalysis will run when you execute your analysis
def my_analysis(context, scope: list):
    # Bellow is an empty filter.
    # Examples of filter:
    # { tags: [{ key: 'tag-key', value: 'tag-value' }]}
    # { name: 'name*' }
    # { name: '*name' }
    # { bucket: 'bucket-id' }
    filter = {}


    resources = Resources()
    devices = resources.devices.listDevice(
        {
            "page": 1,
            "fields": ["id", "type"],
            "filter": filter,
            "amount": 100,
        }
    )

    for device_obj in devices:
        type_device = device_obj.get("type")
        # immutable devices can't have data removed
        if type_device == "immutable":
            continue

        tokens = resources.devices.tokenList(deviceID=device_obj["id"])
        if not tokens:
            continue

        device = Device({"token": tokens[0]["token"]})

        variables = ["temperature"]
        qty = 100  # remove 100 registers of each variable
        end_date = "30 days"  # registers old than 30 days

        result = device.deleteData(
            {"variables": variables, "qty": qty, "end_date": end_date}
        )
        print(result)


# The analysis token in only necessary to run the analysis outside TagoIO
Analysis.use(my_analysis, params={"token": "MY-ANALYSIS-TOKEN-HERE"})
