"""The labels assigned to the tokens in the training data, and used for training the model."""
# Some extra code that is included during the `spacy package` command.

AddressNumber = "AddressNumber"
"""e.g. "123" in "123 Main St"."""
AddressNumberPrefix = "AddressNumberPrefix"
"""e.g. "#" in "#123 Main St" or "Mi" in "Mi 32 Richardson Hwy"."""
AddressNumberSuffix = "AddressNumberSuffix"
"""e.g. "1/2" in "123 1/2 Main St"."""
BuildingName = "BuildingName"
"""e.g. "Tower A" in "Tower A, 123 Main St"."""
CornerOf = "CornerOf"
"""e.g. "Corner of" in "Corner of Main St and Elm St" or "Junction of" in "Junction of Main St and Elm St"."""
CountryName = "CountryName"
"""e.g. "Canada" in "Toronto, Canada"."""
IntersectionSeparator = "IntersectionSeparator"
"""e.g. "&" in "Main St & Elm St"."""
LandmarkName = "LandmarkName"
"""e.g. "Union Station" in "Union Station, Washington, DC"."""
NotAddress = "NotAddress"
"""e.g. "(east side)" in "123 Main St (east side), Chicago IL"."""
OccupancyIdentifier = "OccupancyIdentifier"
"""e.g. "101" in "Suite 101"."""
OccupancyType = "OccupancyType"
"""e.g. "Suite" in "Suite 101"."""
PlaceName = "PlaceName"
"""e.g. "Anchorage" in "4321 Elm St, Anchorage, AK"."""
Recipient = "Recipient"
"""e.g. "C/O John Doe" in "C/O John Doe, 123 Main St"."""
StateName = "StateName"
"""e.g. "Alaska" in "4321 Elm St, Anchorage, Alaska"."""
StreetName = "StreetName"
"""e.g. "Main" in "123 Main St"."""
StreetNamePostDirectional = "StreetNamePostDirectional"
"""e.g. "NW" in "123 Main St NW"."""
StreetNamePostModifier = "StreetNamePostModifier"
"""e.g. "Ext" in "123 Main St Ext"."""
StreetNamePostType = "StreetNamePostType"
"""e.g. "St" in "123 Main St"."""
StreetNamePreDirectional = "StreetNamePreDirectional"
"""e.g. "NW" in "NW 123 Main St"."""
StreetNamePreModifier = "StreetNamePreModifier"
"""e.g. "Old" in "Old Elm St"."""
StreetNamePreType = "StreetNamePreType"
"""e.g. "US Hwy" in "US Hwy 101"."""
SubaddressIdentifier = "SubaddressIdentifier"
"""e.g. "304" in "203 Elm St, Building 304, Honolulu Hawaii" or "22" in "55 5th Ave, PMB 22, New York NY"."""
SubaddressType = "SubaddressType"
"""e.g. "Building" in "203 Elm St, Building 304, Honolulu Hawaii" or "PMB" in "55 5th Ave, PMB 22, New York NY"."""
USPSBoxGroupID = "USPSBoxGroupID"
"""e.g. "1" in "Rural Route 1 Box 2"."""
USPSBoxGroupType = "USPSBoxGroupType"
"""e.g. "Rural Route" in "Rural Route 1 Box 2"."""
USPSBoxID = "USPSBoxID"
"""e.g. "2" in "Rural Route 1 Box 2"."""
USPSBoxType = "USPSBoxType"
"""e.g. "Box" in "Rural Route 1 Box 2"."""
ZipCode = "ZipCode"
"""e.g. "12345" in "12345"."""
ZipPlus4 = "ZipPlus4"
"""e.g. "6789" in "12345-6789"."""
