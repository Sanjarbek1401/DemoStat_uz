import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard_app.models import Region, StatisticsData
from django.db import transaction

# First, get or create the Navoi region
tashkent_region, _ = Region.objects.get_or_create(name='Navoiy', defaults={'svg_id': 'navoi'})

# Data to be imported
navoi_male_data =[
  {
    "2021": "524061",
    "2022": "533353",
    "2023": "542371",
    "2024": "551064",
    "2025": "559480",
    "2026": "567605",
    "2027": "575423",
    "2028": "582975",
    "2029": "590221",
    "2030": "597155",
    "2031": "603758",
    "2032": "610033",
    "2033": "615985",
    "2034": "621593",
    "2035": "626910",
    "2036": "631942",
    "2037": "636756",
    "2038": "641374",
    "2039": "645845",
    "2040": "650234",
    "2041": "654628",
    "2042": "659080",
    "2043": "663614",
    "2044": "668241",
    "2045": "672994",
    "2046": "677857",
    "2047": "682826",
    "2048": "687886",
    "2049": "693016",
    "2050": "698180",
    "Age": "Total"
  },
  {
    "2021": "58869",
    "2022": "61447",
    "2023": "63384",
    "2024": "64801",
    "2025": "65574",
    "2026": "65016",
    "2027": "64749",
    "2028": "64314",
    "2029": "63765",
    "2030": "63075",
    "2031": "62258",
    "2032": "61346",
    "2033": "60319",
    "2034": "59148",
    "2035": "58016",
    "2036": "56855",
    "2037": "55774",
    "2038": "54804",
    "2039": "54028",
    "2040": "53454",
    "2041": "53159",
    "2042": "53134",
    "2043": "53371",
    "2044": "53839",
    "2045": "54500",
    "2046": "55263",
    "2047": "56064",
    "2048": "56873",
    "2049": "57656",
    "2050": "58354",
    "Age": "0-4"
  },
  {
    "2021": "50671",
    "2022": "51632",
    "2023": "52689",
    "2024": "53747",
    "2025": "55294",
    "2026": "57896",
    "2027": "60268",
    "2028": "62049",
    "2029": "63364",
    "2030": "64102",
    "2031": "63570",
    "2032": "63350",
    "2033": "62970",
    "2034": "62488",
    "2035": "61879",
    "2036": "61154",
    "2037": "60342",
    "2038": "59482",
    "2039": "58403",
    "2040": "57353",
    "2041": "56307",
    "2042": "55336",
    "2043": "54466",
    "2044": "53777",
    "2045": "53276",
    "2046": "53035",
    "2047": "53046",
    "2048": "53302",
    "2049": "53773",
    "2050": "54425",
    "Age": "5-9"
  },
  {
    "2021": "45322",
    "2022": "45892",
    "2023": "46820",
    "2024": "47891",
    "2025": "48874",
    "2026": "50031",
    "2027": "50911",
    "2028": "51894",
    "2029": "52874",
    "2030": "54311",
    "2031": "56772",
    "2032": "59011",
    "2033": "60699",
    "2034": "61958",
    "2035": "62689",
    "2036": "62194",
    "2037": "62024",
    "2038": "61697",
    "2039": "61277",
    "2040": "60736",
    "2041": "60087",
    "2042": "59356",
    "2043": "58524",
    "2044": "57595",
    "2045": "56638",
    "2046": "55684",
    "2047": "54800",
    "2048": "54008",
    "2049": "53387",
    "2050": "52940",
    "Age": "10-14"
  },
  {
    "2021": "38439",
    "2022": "39576",
    "2023": "41126",
    "2024": "42343",
    "2025": "43676",
    "2026": "44712",
    "2027": "45220",
    "2028": "46090",
    "2029": "47103",
    "2030": "48029",
    "2031": "49133",
    "2032": "49964",
    "2033": "50903",
    "2034": "51836",
    "2035": "53204",
    "2036": "55565",
    "2037": "57705",
    "2038": "59137",
    "2039": "60529",
    "2040": "61250",
    "2041": "60791",
    "2042": "60668",
    "2043": "60388",
    "2044": "60021",
    "2045": "59540",
    "2046": "58956",
    "2047": "58296",
    "2048": "57538",
    "2049": "56686",
    "2050": "55806",
    "Age": "15-19"
  },
  {
    "2021": "37096",
    "2022": "36830",
    "2023": "36867",
    "2024": "37262",
    "2025": "37801",
    "2026": "38533",
    "2027": "39571",
    "2028": "41004",
    "2029": "42109",
    "2030": "43338",
    "2031": "44293",
    "2032": "44750",
    "2033": "45569",
    "2034": "46526",
    "2035": "47396",
    "2036": "48438",
    "2037": "49213",
    "2038": "50104",
    "2039": "50989",
    "2040": "52277",
    "2041": "54511",
    "2042": "56513",
    "2043": "58019",
    "2044": "59161",
    "2045": "59872",
    "2046": "59466",
    "2047": "59410",
    "2048": "59196",
    "2049": "58903",
    "2050": "58502",
    "Age": "20-24"
  },
  {
    "2021": "47515",
    "2022": "45263",
    "2023": "42567",
    "2024": "40422",
    "2025": "38917",
    "2026": "37818",
    "2027": "37616",
    "2028": "37663",
    "2029": "38037",
    "2030": "38529",
    "2031": "39190",
    "2032": "40121",
    "2033": "41423",
    "2034": "42405",
    "2035": "43522",
    "2036": "44398",
    "2037": "44811",
    "2038": "45582",
    "2039": "46477",
    "2040": "47280",
    "2041": "48255",
    "2042": "48971",
    "2043": "49814",
    "2044": "50642",
    "2045": "51828",
    "2046": "53900",
    "2047": "55736",
    "2048": "57121",
    "2049": "58191",
    "2050": "58899",
    "Age": "25-29"
  },
  {
    "2021": "47565",
    "2022": "47962",
    "2023": "48458",
    "2024": "48339",
    "2025": "48180",
    "2026": "46493",
    "2027": "44519",
    "2028": "42153",
    "2029": "40309",
    "2030": "39035",
    "2031": "38093",
    "2032": "37966",
    "2033": "38031",
    "2034": "38391",
    "2035": "38849",
    "2036": "39454",
    "2037": "40297",
    "2038": "41489",
    "2039": "42371",
    "2040": "43400",
    "2041": "44217",
    "2042": "44602",
    "2043": "45332",
    "2044": "46173",
    "2045": "46923",
    "2046": "47845",
    "2047": "48520",
    "2048": "49322",
    "2049": "50099",
    "2050": "51185",
    "Age": "30-34"
  },
  {
    "2021": "41893",
    "2022": "43368",
    "2023": "44333",
    "2024": "45180",
    "2025": "44838",
    "2026": "45635",
    "2027": "45919",
    "2028": "46352",
    "2029": "46230",
    "2030": "46154",
    "2031": "44682",
    "2032": "43010",
    "2033": "40968",
    "2034": "39405",
    "2035": "38344",
    "2036": "37548",
    "2037": "37491",
    "2038": "37582",
    "2039": "37940",
    "2040": "38377",
    "2041": "38943",
    "2042": "39717",
    "2043": "40822",
    "2044": "41626",
    "2045": "42587",
    "2046": "43361",
    "2047": "43729",
    "2048": "44431",
    "2049": "45228",
    "2050": "45932",
    "Age": "35-39"
  },
  {
    "2021": "34036",
    "2022": "35380",
    "2023": "36440",
    "2024": "37542",
    "2025": "38936",
    "2026": "40121",
    "2027": "41412",
    "2028": "42243",
    "2029": "43024",
    "2030": "42669",
    "2031": "43428",
    "2032": "43678",
    "2033": "44106",
    "2034": "44020",
    "2035": "44039",
    "2036": "42754",
    "2037": "41322",
    "2038": "39530",
    "2039": "38174",
    "2040": "37267",
    "2041": "36576",
    "2042": "36572",
    "2043": "36826",
    "2044": "37044",
    "2045": "37470",
    "2046": "38010",
    "2047": "38738",
    "2048": "39872",
    "2049": "40533",
    "2050": "41446",
    "Age": "40-44"
  },
  {
    "2021": "29080",
    "2022": "29133",
    "2023": "29898",
    "2024": "30919",
    "2025": "31872",
    "2026": "32802",
    "2027": "34012",
    "2028": "34957",
    "2029": "35947",
    "2030": "37222",
    "2031": "38297",
    "2032": "39493",
    "2033": "40258",
    "2034": "41014",
    "2035": "40678",
    "2036": "41428",
    "2037": "41673",
    "2038": "42109",
    "2039": "42059",
    "2040": "42142",
    "2041": "40993",
    "2042": "39734",
    "2043": "38123",
    "2044": "36923",
    "2045": "36132",
    "2046": "35523",
    "2047": "35563",
    "2048": "35694",
    "2049": "36058",
    "2050": "36476",
    "Age": "45-49"
  },
  {
    "2021": "27144",
    "2022": "28211",
    "2023": "27593",
    "2024": "26921",
    "2025": "27080",
    "2026": "27874",
    "2027": "27891",
    "2028": "28593",
    "2029": "29531",
    "2030": "30404",
    "2031": "31258",
    "2032": "32382",
    "2033": "33254",
    "2034": "34173",
    "2035": "35367",
    "2036": "36369",
    "2037": "37498",
    "2038": "38220",
    "2039": "38962",
    "2040": "38650",
    "2041": "39397",
    "2042": "39645",
    "2043": "40092",
    "2044": "40074",
    "2045": "40206",
    "2046": "39172",
    "2047": "38055",
    "2048": "36596",
    "2049": "35523",
    "2050": "34828",
    "Age": "50-54"
  },
  {
    "2021": "22747",
    "2022": "22717",
    "2023": "23288",
    "2024": "25001",
    "2025": "25749",
    "2026": "25811",
    "2027": "26550",
    "2028": "25985",
    "2029": "25388",
    "2030": "25552",
    "2031": "26304",
    "2032": "26318",
    "2033": "26979",
    "2034": "27854",
    "2035": "28667",
    "2036": "29462",
    "2037": "30512",
    "2038": "31325",
    "2039": "32185",
    "2040": "33308",
    "2041": "34246",
    "2042": "35314",
    "2043": "35995",
    "2044": "36723",
    "2045": "36444",
    "2046": "37190",
    "2047": "37446",
    "2048": "37902",
    "2049": "37915",
    "2050": "38085",
    "Age": "55-59"
  },
  {
    "2021": "19168",
    "2022": "19926",
    "2023": "20435",
    "2024": "20743",
    "2025": "20697",
    "2026": "20669",
    "2027": "20630",
    "2028": "21638",
    "2029": "22687",
    "2030": "23349",
    "2031": "23389",
    "2032": "24082",
    "2033": "23604",
    "2034": "23116",
    "2035": "23301",
    "2036": "24014",
    "2037": "24040",
    "2038": "24666",
    "2039": "25475",
    "2040": "26228",
    "2041": "26965",
    "2042": "27932",
    "2043": "28684",
    "2044": "29483",
    "2045": "30530",
    "2046": "31400",
    "2047": "32398",
    "2048": "33036",
    "2049": "33743",
    "2050": "33501",
    "Age": "60-64"
  },
  {
    "2021": "11743",
    "2022": "12503",
    "2023": "13510",
    "2024": "14525",
    "2025": "15452",
    "2026": "16436",
    "2027": "17065",
    "2028": "17493",
    "2029": "17777",
    "2030": "17755",
    "2031": "17767",
    "2032": "17748",
    "2033": "18656",
    "2034": "19590",
    "2035": "20183",
    "2036": "20228",
    "2037": "20881",
    "2038": "20508",
    "2039": "20136",
    "2040": "20340",
    "2041": "21009",
    "2042": "21055",
    "2043": "21642",
    "2044": "22385",
    "2045": "23077",
    "2046": "23755",
    "2047": "24638",
    "2048": "25330",
    "2049": "26067",
    "2050": "27029",
    "Age": "65-69"
  },
  {
    "2021": "6679",
    "2022": "7372",
    "2023": "7876",
    "2024": "8425",
    "2025": "8866",
    "2026": "9516",
    "2027": "10129",
    "2028": "10947",
    "2029": "11774",
    "2030": "12532",
    "2031": "13353",
    "2032": "13882",
    "2033": "14261",
    "2034": "14525",
    "2035": "14539",
    "2036": "14599",
    "2037": "14611",
    "2038": "15421",
    "2039": "16243",
    "2040": "16767",
    "2041": "16821",
    "2042": "17416",
    "2043": "17147",
    "2044": "16887",
    "2045": "17107",
    "2046": "17721",
    "2047": "17790",
    "2048": "18332",
    "2049": "19003",
    "2050": "19628",
    "Age": "70-74"
  },
  {
    "2021": "3069",
    "2022": "3216",
    "2023": "3551",
    "2024": "3953",
    "2025": "4554",
    "2026": "4968",
    "2027": "5478",
    "2028": "5864",
    "2029": "6282",
    "2030": "6631",
    "2031": "7138",
    "2032": "7625",
    "2033": "8267",
    "2034": "8921",
    "2035": "9524",
    "2036": "10187",
    "2037": "10623",
    "2038": "10950",
    "2039": "11196",
    "2040": "11241",
    "2041": "11342",
    "2042": "11384",
    "2043": "12087",
    "2044": "12790",
    "2045": "13237",
    "2046": "13300",
    "2047": "13818",
    "2048": "13650",
    "2049": "13498",
    "2050": "13722",
    "Age": "75-79"
  },
  {
    "2021": "1945",
    "2022": "2038",
    "2023": "1977",
    "2024": "1946",
    "2025": "1973",
    "2026": "1976",
    "2027": "2091",
    "2028": "2318",
    "2029": "2585",
    "2030": "2991",
    "2031": "3269",
    "2032": "3622",
    "2033": "3890",
    "2034": "4186",
    "2035": "4449",
    "2036": "4819",
    "2037": "5181",
    "2038": "5650",
    "2039": "6130",
    "2040": "6576",
    "2041": "7075",
    "2042": "7410",
    "2043": "7676",
    "2044": "7891",
    "2045": "7958",
    "2046": "8084",
    "2047": "8150",
    "2048": "8722",
    "2049": "9286",
    "2050": "9640",
    "Age": "80-84"
  },
  {
    "2021": "810",
    "2022": "903",
    "2023": "1018",
    "2024": "1103",
    "2025": "1149",
    "2026": "1299",
    "2027": "1391",
    "2028": "1411",
    "2029": "1436",
    "2030": "1476",
    "2031": "1564",
    "2032": "1684",
    "2033": "1829",
    "2034": "2000",
    "2035": "2264",
    "2036": "2476",
    "2037": "2756",
    "2038": "2997",
    "2039": "3273",
    "2040": "3585",
    "2041": "3933",
    "2042": "4319",
    "2043": "4749",
    "2044": "5208",
    "2045": "5669",
    "2046": "6190",
    "2047": "6629",
    "2048": "7053",
    "2049": "7467",
    "2050": "7783",
    "Age": "85+"
  }
]
# Convert age ranges to min/max values
def get_age_min_max(age_str):
    if age_str == "Total":
        return 0, None  # For total population, use 0 as min age
    elif age_str == "85+":
        return 85, None
    elif '-' in age_str:
        age_parts = age_str.split('-')
        return int(age_parts[0]), int(age_parts[1])
    return None, None

# Delete existing Navoi male data
StatisticsData.objects.filter(region=tashkent_region, gender='erkak').delete()

# Import new data
with transaction.atomic():
    for entry in navoi_male_data:
        age_min, age_max = get_age_min_max(entry['Age'])
        for year in range(2021, 2051):
            year_str = str(year)
            if year_str in entry:
                population = int(entry[year_str])
                StatisticsData.objects.create(
                    region=tashkent_region,
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    gender='erkak',
                    population=population
                )

print("Navoi male data import completed successfully!")
