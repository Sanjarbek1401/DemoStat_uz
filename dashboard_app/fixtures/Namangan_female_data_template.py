import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard_app.models import Region, StatisticsData
from django.db import transaction

# First, get or create the Navoi region
tashkent_city_region, _ = Region.objects.get_or_create(name='Namangan', defaults={'svg_id': 'namangan'})

# Data to be imported
navoi_male_data = [
  {
    "2021": "1442007",
    "2022": "1473489",
    "2023": "1504723",
    "2024": "1535376",
    "2025": "1565451",
    "2026": "1594929",
    "2027": "1623808",
    "2028": "1652072",
    "2029": "1679460",
    "2030": "1705875",
    "2031": "1731225",
    "2032": "1755549",
    "2033": "1778954",
    "2034": "1801366",
    "2035": "1822948",
    "2036": "1843732",
    "2037": "1863945",
    "2038": "1883706",
    "2039": "1903191",
    "2040": "1922627",
    "2041": "1942286",
    "2042": "1962345",
    "2043": "1982860",
    "2044": "2003860",
    "2045": "2025408",
    "2046": "2047441",
    "2047": "2069880",
    "2048": "2092646",
    "2049": "2115601",
    "2050": "2138601",
    "Age": "Total"
  },
  {
    "2021": "167118",
    "2022": "176679",
    "2023": "183862",
    "2024": "187837",
    "2025": "189807",
    "2026": "189097",
    "2027": "187594",
    "2028": "185734",
    "2029": "183594",
    "2030": "181080",
    "2031": "178120",
    "2032": "174755",
    "2033": "171103",
    "2034": "167351",
    "2035": "163765",
    "2036": "160468",
    "2037": "157646",
    "2038": "155326",
    "2039": "153748",
    "2040": "152969",
    "2041": "153223",
    "2042": "154451",
    "2043": "156582",
    "2044": "159468",
    "2045": "162950",
    "2046": "166700",
    "2047": "170460",
    "2048": "174098",
    "2049": "177456",
    "2050": "180319",
    "Age": "0-4"
  },
  {
    "2021": "137410",
    "2022": "142253",
    "2023": "146263",
    "2024": "150850",
    "2025": "157699",
    "2026": "166342",
    "2027": "175825",
    "2028": "182956",
    "2029": "186911",
    "2030": "188885",
    "2031": "188199",
    "2032": "186732",
    "2033": "184910",
    "2034": "182812",
    "2035": "180343",
    "2036": "177432",
    "2037": "174121",
    "2038": "170524",
    "2039": "166826",
    "2040": "163294",
    "2041": "160049",
    "2042": "157275",
    "2043": "154998",
    "2044": "153457",
    "2045": "152706",
    "2046": "152978",
    "2047": "154216",
    "2048": "156349",
    "2049": "159229",
    "2050": "162701",
    "Age": "5-9"
  },
  {
    "2021": "124116",
    "2022": "122791",
    "2023": "123796",
    "2024": "128409",
    "2025": "132594",
    "2026": "137003",
    "2027": "141816",
    "2028": "145800",
    "2029": "150358",
    "2030": "157165",
    "2031": "165757",
    "2032": "175189",
    "2033": "182286",
    "2034": "186228",
    "2035": "188208",
    "2036": "187544",
    "2037": "186106",
    "2038": "184317",
    "2039": "182254",
    "2040": "179824",
    "2041": "176955",
    "2042": "173688",
    "2043": "170137",
    "2044": "166484",
    "2045": "162995",
    "2046": "159788",
    "2047": "157047",
    "2048": "154798",
    "2049": "153278",
    "2050": "152542",
    "Age": "10-14"
  },
  {
    "2021": "101537",
    "2022": "105764",
    "2023": "112081",
    "2024": "115919",
    "2025": "119584",
    "2026": "123655",
    "2027": "122327",
    "2028": "123337",
    "2029": "127937",
    "2030": "132103",
    "2031": "136491",
    "2032": "141273",
    "2033": "145231",
    "2034": "149769",
    "2035": "156547",
    "2036": "165097",
    "2037": "174480",
    "2038": "181537",
    "2039": "185463",
    "2040": "187447",
    "2041": "186807",
    "2042": "185405",
    "2043": "183656",
    "2044": "181634",
    "2045": "179245",
    "2046": "176418",
    "2047": "173192",
    "2048": "169681",
    "2049": "166068",
    "2050": "162614",
    "Age": "15-19"
  },
  {
    "2021": "104008",
    "2022": "102380",
    "2023": "100939",
    "2024": "99806",
    "2025": "100846",
    "2026": "101657",
    "2027": "105835",
    "2028": "112042",
    "2029": "115754",
    "2030": "119281",
    "2031": "123249",
    "2032": "121950",
    "2033": "123021",
    "2034": "127602",
    "2035": "131695",
    "2036": "135972",
    "2037": "140632",
    "2038": "144526",
    "2039": "149033",
    "2040": "155734",
    "2041": "164140",
    "2042": "173341",
    "2043": "180258",
    "2044": "184126",
    "2045": "186128",
    "2046": "185574",
    "2047": "184289",
    "2048": "182661",
    "2049": "180755",
    "2050": "178480",
    "Age": "20-24"
  },
  {
    "2021": "133991",
    "2022": "128995",
    "2023": "122483",
    "2024": "118137",
    "2025": "110725",
    "2026": "104479",
    "2027": "103022",
    "2028": "101702",
    "2029": "100658",
    "2030": "101737",
    "2031": "102530",
    "2032": "106572",
    "2033": "112582",
    "2034": "116161",
    "2035": "119602",
    "2036": "123546",
    "2037": "122310",
    "2038": "123387",
    "2039": "127874",
    "2040": "131868",
    "2041": "136070",
    "2042": "140767",
    "2043": "144524",
    "2044": "148947",
    "2045": "155497",
    "2046": "163700",
    "2047": "172700",
    "2048": "179488",
    "2049": "183315",
    "2050": "185349",
    "Age": "25-29"
  },
  {
    "2021": "128557",
    "2022": "131257",
    "2023": "133452",
    "2024": "134696",
    "2025": "134719",
    "2026": "132923",
    "2027": "128121",
    "2028": "121848",
    "2029": "117733",
    "2030": "110584",
    "2031": "104559",
    "2032": "103224",
    "2033": "101986",
    "2034": "101001",
    "2035": "102102",
    "2036": "102883",
    "2037": "106841",
    "2038": "112740",
    "2039": "116254",
    "2040": "119656",
    "2041": "123593",
    "2042": "122415",
    "2043": "123516",
    "2044": "127968",
    "2045": "131920",
    "2046": "136082",
    "2047": "140643",
    "2048": "144440",
    "2049": "148787",
    "2050": "155216",
    "Age": "30-34"
  },
  {
    "2021": "109800",
    "2022": "113666",
    "2023": "117823",
    "2024": "120724",
    "2025": "124169",
    "2026": "127101",
    "2027": "129742",
    "2028": "131907",
    "2029": "133156",
    "2030": "133226",
    "2031": "131536",
    "2032": "126909",
    "2033": "120837",
    "2034": "116908",
    "2035": "109966",
    "2036": "104117",
    "2037": "102876",
    "2038": "101707",
    "2039": "100776",
    "2040": "101904",
    "2041": "102691",
    "2042": "106604",
    "2043": "112433",
    "2044": "115909",
    "2045": "119288",
    "2046": "123220",
    "2047": "122083",
    "2048": "123195",
    "2049": "127602",
    "2050": "131499",
    "Age": "35-39"
  },
  {
    "2021": "90404",
    "2022": "93895",
    "2023": "96718",
    "2024": "99782",
    "2025": "104175",
    "2026": "108503",
    "2027": "112289",
    "2028": "116379",
    "2029": "119232",
    "2030": "122631",
    "2031": "125528",
    "2032": "128143",
    "2033": "130304",
    "2034": "131566",
    "2035": "131679",
    "2036": "130071",
    "2037": "125581",
    "2038": "119663",
    "2039": "115873",
    "2040": "109093",
    "2041": "103382",
    "2042": "102216",
    "2043": "101103",
    "2044": "100221",
    "2045": "101371",
    "2046": "102164",
    "2047": "106040",
    "2048": "111807",
    "2049": "115246",
    "2050": "118595",
    "Age": "40-44"
  },
  {
    "2021": "84818",
    "2022": "85050",
    "2023": "84986",
    "2024": "86314",
    "2025": "87236",
    "2026": "89167",
    "2027": "92603",
    "2028": "95381",
    "2029": "98398",
    "2030": "102725",
    "2031": "106993",
    "2032": "110727",
    "2033": "114767",
    "2034": "117588",
    "2035": "120956",
    "2036": "123833",
    "2037": "126436",
    "2038": "128594",
    "2039": "129869",
    "2040": "130023",
    "2041": "128491",
    "2042": "124119",
    "2043": "118338",
    "2044": "114664",
    "2045": "108027",
    "2046": "102438",
    "2047": "101330",
    "2048": "100260",
    "2049": "99413",
    "2050": "100571",
    "Age": "45-49"
  },
  {
    "2021": "71398",
    "2022": "73920",
    "2023": "76625",
    "2024": "79734",
    "2025": "81766",
    "2026": "83188",
    "2027": "83426",
    "2028": "83383",
    "2029": "84707",
    "2030": "85631",
    "2031": "87549",
    "2032": "90934",
    "2033": "93675",
    "2034": "96652",
    "2035": "100916",
    "2036": "105128",
    "2037": "108814",
    "2038": "112805",
    "2039": "115596",
    "2040": "118937",
    "2041": "121799",
    "2042": "124393",
    "2043": "126552",
    "2044": "127841",
    "2045": "128036",
    "2046": "126578",
    "2047": "122319",
    "2048": "116670",
    "2049": "113101",
    "2050": "106606",
    "Age": "50-54"
  },
  {
    "2021": "64150",
    "2022": "64450",
    "2023": "65790",
    "2024": "65561",
    "2025": "67001",
    "2026": "69271",
    "2027": "71729",
    "2028": "74376",
    "2029": "77398",
    "2030": "79389",
    "2031": "80802",
    "2032": "81058",
    "2033": "81058",
    "2034": "82385",
    "2035": "83323",
    "2036": "85233",
    "2037": "88558",
    "2038": "91255",
    "2039": "94185",
    "2040": "98374",
    "2041": "102519",
    "2042": "106147",
    "2043": "110074",
    "2044": "112827",
    "2045": "116134",
    "2046": "118979",
    "2047": "121552",
    "2048": "123701",
    "2049": "124987",
    "2050": "125220",
    "Age": "55-59"
  },
  {
    "2021": "53283",
    "2022": "56014",
    "2023": "57507",
    "2024": "59194",
    "2025": "59975",
    "2026": "60717",
    "2027": "61032",
    "2028": "62349",
    "2029": "62166",
    "2030": "63589",
    "2031": "65804",
    "2032": "68182",
    "2033": "70763",
    "2034": "73665",
    "2035": "75609",
    "2036": "77018",
    "2037": "77307",
    "2038": "77377",
    "2039": "78709",
    "2040": "79673",
    "2041": "81578",
    "2042": "84816",
    "2043": "87455",
    "2044": "90323",
    "2045": "94402",
    "2046": "98452",
    "2047": "101991",
    "2048": "105814",
    "2049": "108498",
    "2050": "111720",
    "Age": "60-64"
  },
  {
    "2021": "32035",
    "2022": "34561",
    "2023": "38412",
    "2024": "42038",
    "2025": "45724",
    "2026": "48326",
    "2027": "50835",
    "2028": "52240",
    "2029": "53832",
    "2030": "54617",
    "2031": "55372",
    "2032": "55732",
    "2033": "57032",
    "2034": "56937",
    "2035": "58347",
    "2036": "60491",
    "2037": "62765",
    "2038": "65252",
    "2039": "67991",
    "2040": "69871",
    "2041": "71274",
    "2042": "71616",
    "2043": "71789",
    "2044": "73129",
    "2045": "74128",
    "2046": "76019",
    "2047": "79125",
    "2048": "81670",
    "2049": "84434",
    "2050": "88337",
    "Age": "65-69"
  },
  {
    "2021": "19614",
    "2022": "21115",
    "2023": "22466",
    "2024": "23831",
    "2025": "25015",
    "2026": "27433",
    "2027": "29665",
    "2028": "33038",
    "2029": "36202",
    "2030": "39444",
    "2031": "41772",
    "2032": "44018",
    "2033": "45329",
    "2034": "46814",
    "2035": "47614",
    "2036": "48393",
    "2037": "48819",
    "2038": "50091",
    "2039": "50110",
    "2040": "51489",
    "2041": "53527",
    "2042": "55658",
    "2043": "58013",
    "2044": "60536",
    "2045": "62327",
    "2046": "63708",
    "2047": "64107",
    "2048": "64392",
    "2049": "65715",
    "2050": "66734",
    "Age": "70-74"
  },
  {
    "2021": "9666",
    "2022": "10168",
    "2023": "11079",
    "2024": "12122",
    "2025": "13936",
    "2026": "15176",
    "2027": "16395",
    "2028": "17469",
    "2029": "18566",
    "2030": "19593",
    "2031": "21610",
    "2032": "23475",
    "2033": "26251",
    "2034": "28845",
    "2035": "31536",
    "2036": "33519",
    "2037": "35430",
    "2038": "36613",
    "2039": "37942",
    "2040": "38736",
    "2041": "39515",
    "2042": "39995",
    "2043": "41201",
    "2044": "41339",
    "2045": "42651",
    "2046": "44519",
    "2047": "46432",
    "2048": "48577",
    "2049": "50778",
    "2050": "52407",
    "Age": "75-79"
  },
  {
    "2021": "6545",
    "2022": "6796",
    "2023": "6524",
    "2024": "6280",
    "2025": "6337",
    "2026": "6343",
    "2027": "6768",
    "2028": "7409",
    "2029": "8141",
    "2030": "9426",
    "2031": "10319",
    "2032": "11221",
    "2033": "11999",
    "2034": "12809",
    "2035": "13638",
    "2036": "15181",
    "2037": "16615",
    "2038": "18701",
    "2039": "20640",
    "2040": "22683",
    "2041": "24238",
    "2042": "25734",
    "2043": "26728",
    "2044": "27838",
    "2045": "28577",
    "2046": "29306",
    "2047": "29802",
    "2048": "30868",
    "2049": "31096",
    "2050": "32256",
    "Age": "80-84"
  },
  {
    "2021": "3557",
    "2022": "3737",
    "2023": "3918",
    "2024": "4142",
    "2025": "4145",
    "2026": "4547",
    "2027": "4784",
    "2028": "4723",
    "2029": "4718",
    "2030": "4769",
    "2031": "5035",
    "2032": "5453",
    "2033": "5819",
    "2034": "6274",
    "2035": "7101",
    "2036": "7807",
    "2037": "8609",
    "2038": "9291",
    "2039": "10048",
    "2040": "11052",
    "2041": "12435",
    "2042": "13796",
    "2043": "15503",
    "2044": "17149",
    "2045": "19025",
    "2046": "20817",
    "2047": "22552",
    "2048": "24178",
    "2049": "25844",
    "2050": "27415",
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
StatisticsData.objects.filter(region=tashkent_city_region, gender='ayol').delete()

# Import new data
with transaction.atomic():
    for entry in navoi_male_data:
        age_min, age_max = get_age_min_max(entry['Age'])
        for year in range(2021, 2051):
            year_str = str(year)
            if year_str in entry:
                population = int(entry[year_str])
                StatisticsData.objects.create(
                    region=tashkent_city_region,
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    gender='ayol',
                    population=population
                )

print("Navoi female data import completed successfully!")
