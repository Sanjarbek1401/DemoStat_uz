import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard_app.models import Region, StatisticsData
from django.db import transaction

# First, get or create the Navoi region
tashkent_city_region, _ = Region.objects.get_or_create(name='Toshkent', defaults={'svg_id': 'tashkent'})

# Data to be imported
navoi_male_data = [
  {
    "Age": "Total",
    "2022": "1464920",
    "2023": "1486656",
    "2024": "1507983",
    "2025": "1528720",
    "2026": "1548907",
    "2027": "1568480",
    "2028": "1587386",
    "2029": "1605705",
    "2030": "1623352",
    "2031": "1640270",
    "2032": "1656359",
    "2033": "1671554",
    "2034": "1685820",
    "2035": "1699041",
    "2036": "1711348",
    "2037": "1722726",
    "2038": "1733331",
    "2039": "1743235",
    "2040": "1752581",
    "2041": "1761555",
    "2042": "1770398",
    "2043": "1779273",
    "2044": "1788257",
    "2045": "1797409",
    "2046": "1806799",
    "2047": "1816422",
    "2048": "1826245",
    "2049": "1836240",
    "2050": "1846351"
  },
  {
    "Age": "0-4",
    "2022": "142953",
    "2023": "152051",
    "2024": "158797",
    "2025": "162916",
    "2026": "165099",
    "2027": "164727",
    "2028": "163374",
    "2029": "161719",
    "2030": "159909",
    "2031": "157850",
    "2032": "155513",
    "2033": "152895",
    "2034": "149878",
    "2035": "146457",
    "2036": "142828",
    "2037": "139107",
    "2038": "135507",
    "2039": "132145",
    "2040": "129266",
    "2041": "126933",
    "2042": "125377",
    "2043": "124611",
    "2044": "124627",
    "2045": "125338",
    "2046": "126637",
    "2047": "128278",
    "2048": "130068",
    "2049": "131907",
    "2050": "133682"
  },
  {
    "Age": "5-9",
    "2022": "126568",
    "2023": "126185",
    "2024": "127924",
    "2025": "130376",
    "2026": "134320",
    "2027": "141334",
    "2028": "150175",
    "2029": "156727",
    "2030": "160741",
    "2031": "162904",
    "2032": "162579",
    "2033": "161310",
    "2034": "159751",
    "2035": "158037",
    "2036": "156080",
    "2037": "153848",
    "2038": "151343",
    "2039": "148449",
    "2040": "145164",
    "2041": "141680",
    "2042": "138110",
    "2043": "134663",
    "2044": "131448",
    "2045": "128703",
    "2046": "126484",
    "2047": "125018",
    "2048": "124313",
    "2049": "124365",
    "2050": "125087"
  },
  {
    "Age": "10-14",
    "2022": "125310",
    "2023": "125207",
    "2024": "124208",
    "2025": "123582",
    "2026": "124573",
    "2027": "125452",
    "2028": "125062",
    "2029": "126774",
    "2030": "129168",
    "2031": "133013",
    "2032": "139873",
    "2033": "148540",
    "2034": "154962",
    "2035": "158907",
    "2036": "161054",
    "2037": "160760",
    "2038": "159549",
    "2039": "158056",
    "2040": "156416",
    "2041": "154542",
    "2042": "152404",
    "2043": "150007",
    "2044": "147234",
    "2045": "144076",
    "2046": "140723",
    "2047": "137279",
    "2048": "133950",
    "2049": "130839",
    "2050": "128182"
  },
  {
    "Age": "15-19",
    "2022": "103256",
    "2023": "107050",
    "2024": "112916",
    "2025": "117415",
    "2026": "121606",
    "2027": "123891",
    "2028": "123750",
    "2029": "122770",
    "2030": "122189",
    "2031": "123215",
    "2032": "124115",
    "2033": "123736",
    "2034": "125427",
    "2035": "127785",
    "2036": "131575",
    "2037": "138319",
    "2038": "146810",
    "2039": "153069",
    "2040": "156914",
    "2041": "159020",
    "2042": "158753",
    "2043": "157615",
    "2044": "156213",
    "2045": "154671",
    "2046": "152896",
    "2047": "150860",
    "2048": "148563",
    "2049": "145890",
    "2050": "142835"
  },
  {
    "Age": "20-24",
    "2022": "101587",
    "2023": "99070",
    "2024": "97191",
    "2025": "99194",
    "2026": "100303",
    "2027": "102607",
    "2028": "106060",
    "2029": "111475",
    "2030": "115507",
    "2031": "119199",
    "2032": "121125",
    "2033": "120960",
    "2034": "120220",
    "2035": "119926",
    "2036": "121065",
    "2037": "121928",
    "2038": "121493",
    "2039": "123148",
    "2040": "125499",
    "2041": "129161",
    "2042": "135432",
    "2043": "143190",
    "2044": "148812",
    "2045": "152284",
    "2046": "154283",
    "2047": "154160",
    "2048": "153303",
    "2049": "152205",
    "2050": "150959"
  },
  {
    "Age": "25-29",
    "2022": "120555",
    "2023": "117848",
    "2024": "114686",
    "2025": "110635",
    "2026": "105956",
    "2027": "102111",
    "2028": "100126",
    "2029": "98514",
    "2030": "100489",
    "2031": "101474",
    "2032": "103552",
    "2033": "106519",
    "2034": "111279",
    "2035": "114715",
    "2036": "118018",
    "2037": "119848",
    "2038": "119835",
    "2039": "119311",
    "2040": "119121",
    "2041": "120260",
    "2042": "121223",
    "2043": "120987",
    "2044": "122698",
    "2045": "124880",
    "2046": "128121",
    "2047": "133688",
    "2048": "140666",
    "2049": "145725",
    "2050": "148916"
  },
  {
    "Age": "30-34",
    "2022": "129031",
    "2023": "127009",
    "2024": "124711",
    "2025": "122549",
    "2026": "120942",
    "2027": "117709",
    "2028": "115396",
    "2029": "112720",
    "2030": "109266",
    "2031": "105219",
    "2032": "101897",
    "2033": "100276",
    "2034": "98842",
    "2035": "100793",
    "2036": "101691",
    "2037": "103606",
    "2038": "106264",
    "2039": "110632",
    "2040": "113739",
    "2041": "116844",
    "2042": "118647",
    "2043": "118771",
    "2044": "118445",
    "2045": "118404",
    "2046": "119628",
    "2047": "120699",
    "2048": "120574",
    "2049": "122269",
    "2050": "124299"
  },
  {
    "Age": "35-39",
    "2022": "117086",
    "2023": "121461",
    "2024": "123735",
    "2025": "124981",
    "2026": "124683",
    "2027": "124340",
    "2028": "122475",
    "2029": "120434",
    "2030": "118546",
    "2031": "117232",
    "2032": "114342",
    "2033": "112374",
    "2034": "110063",
    "2035": "107023",
    "2036": "103395",
    "2037": "100409",
    "2038": "99010",
    "2039": "97679",
    "2040": "99603",
    "2041": "100449",
    "2042": "102286",
    "2043": "104789",
    "2044": "108953",
    "2045": "111899",
    "2046": "114917",
    "2047": "116731",
    "2048": "116955",
    "2049": "116744",
    "2050": "116764"
  },
  {
    "Age": "40-44",
    "2022": "93755",
    "2023": "97125",
    "2024": "99877",
    "2025": "103482",
    "2026": "108379",
    "2027": "113234",
    "2028": "117327",
    "2029": "119467",
    "2030": "120700",
    "2031": "120469",
    "2032": "120244",
    "2033": "118564",
    "2034": "116738",
    "2035": "115045",
    "2036": "113909",
    "2037": "111223",
    "2038": "109456",
    "2039": "107365",
    "2040": "104584",
    "2041": "101230",
    "2042": "98472",
    "2043": "97242",
    "2044": "96013",
    "2045": "97955",
    "2046": "98804",
    "2047": "100614",
    "2048": "103021",
    "2049": "107039",
    "2050": "109857"
  },
  {
    "Age": "45-49",
    "2022": "80514",
    "2023": "81836",
    "2024": "85330",
    "2025": "87852",
    "2026": "89340",
    "2027": "91289",
    "2028": "94501",
    "2029": "97107",
    "2030": "100543",
    "2031": "105236",
    "2032": "109896",
    "2033": "113847",
    "2034": "115930",
    "2035": "117167",
    "2036": "116987",
    "2037": "116838",
    "2038": "115276",
    "2039": "113588",
    "2040": "112023",
    "2041": "111015",
    "2042": "108491",
    "2043": "106886",
    "2044": "104971",
    "2045": "102393",
    "2046": "99250",
    "2047": "96666",
    "2048": "95557",
    "2049": "94396",
    "2050": "96332"
  },
  {
    "Age": "50-54",
    "2022": "76854",
    "2023": "77096",
    "2024": "76367",
    "2025": "77257",
    "2026": "77724",
    "2027": "78257",
    "2028": "79509",
    "2029": "82879",
    "2030": "85306",
    "2031": "86746",
    "2032": "88637",
    "2033": "91751",
    "2034": "94268",
    "2035": "97583",
    "2036": "102111",
    "2037": "106604",
    "2038": "110429",
    "2039": "112453",
    "2040": "113686",
    "2041": "113553",
    "2042": "113482",
    "2043": "112043",
    "2044": "110494",
    "2045": "109059",
    "2046": "108177",
    "2047": "105803",
    "2048": "104330",
    "2049": "102545",
    "2050": "100111"
  },
  {
    "Age": "55-59",
    "2022": "76139",
    "2023": "74925",
    "2024": "74200",
    "2025": "72780",
    "2026": "73174",
    "2027": "73848",
    "2028": "74092",
    "2029": "73409",
    "2030": "74293",
    "2031": "74781",
    "2032": "75341",
    "2033": "76559",
    "2034": "79814",
    "2035": "82150",
    "2036": "83546",
    "2037": "85377",
    "2038": "88383",
    "2039": "90811",
    "2040": "94001",
    "2041": "98359",
    "2042": "102687",
    "2043": "106391",
    "2044": "108373",
    "2045": "109617",
    "2046": "109554",
    "2047": "109577",
    "2048": "108269",
    "2049": "106850",
    "2050": "105531"
  },
  {
    "Age": "60-64",
    "2022": "66322",
    "2023": "68760",
    "2024": "69998",
    "2025": "71252",
    "2026": "71298",
    "2027": "71086",
    "2028": "69976",
    "2029": "69366",
    "2030": "68083",
    "2031": "68531",
    "2032": "69238",
    "2033": "69524",
    "2034": "68929",
    "2035": "69817",
    "2036": "70345",
    "2037": "70942",
    "2038": "72121",
    "2039": "75233",
    "2040": "77464",
    "2041": "78818",
    "2042": "80595",
    "2043": "83487",
    "2044": "85840",
    "2045": "88909",
    "2046": "93085",
    "2047": "97231",
    "2048": "100790",
    "2049": "102713",
    "2050": "103945"
  },
  {
    "Age": "65-69",
    "2022": "45748",
    "2023": "47996",
    "2024": "51663",
    "2025": "54085",
    "2026": "56854",
    "2027": "59399",
    "2028": "61604",
    "2029": "62758",
    "2030": "63941",
    "2031": "64049",
    "2032": "63958",
    "2033": "63043",
    "2034": "62616",
    "2035": "61538",
    "2036": "62068",
    "2037": "62823",
    "2038": "63163",
    "2039": "62690",
    "2040": "63583",
    "2041": "64168",
    "2042": "64827",
    "2043": "65980",
    "2044": "68934",
    "2045": "71060",
    "2046": "72388",
    "2047": "74112",
    "2048": "76863",
    "2049": "79121",
    "2050": "82027"
  },
  {
    "Age": "70-74",
    "2022": "29416",
    "2023": "31737",
    "2024": "33406",
    "2025": "35081",
    "2026": "36286",
    "2027": "38796",
    "2028": "40742",
    "2029": "43933",
    "2030": "46041",
    "2031": "48490",
    "2032": "50755",
    "2033": "52742",
    "2034": "53846",
    "2035": "54973",
    "2036": "55180",
    "2037": "55232",
    "2038": "54552",
    "2039": "54328",
    "2040": "53492",
    "2041": "54101",
    "2042": "54909",
    "2043": "55317",
    "2044": "55005",
    "2045": "55904",
    "2046": "56562",
    "2047": "57290",
    "2048": "58407",
    "2049": "61149",
    "2050": "63129"
  },
  {
    "Age": "75-79",
    "2022": "14862",
    "2023": "15322",
    "2024": "16757",
    "2025": "18975",
    "2026": "21652",
    "2027": "22924",
    "2028": "24787",
    "2029": "26116",
    "2030": "27515",
    "2031": "28588",
    "2032": "30665",
    "2033": "32317",
    "2034": "34986",
    "2035": "36769",
    "2036": "38867",
    "2037": "40817",
    "2038": "42550",
    "2039": "43592",
    "2040": "44633",
    "2041": "44935",
    "2042": "45133",
    "2043": "44710",
    "2044": "44702",
    "2045": "44142",
    "2046": "44827",
    "2047": "45675",
    "2048": "46134",
    "2049": "45985",
    "2050": "46846"
  },
  {
    "Age": "80-84",
    "2022": "10315",
    "2023": "11016",
    "2024": "10803",
    "2025": "10371",
    "2026": "10280",
    "2027": "10030",
    "2028": "10455",
    "2029": "11493",
    "2030": "13070",
    "2031": "15007",
    "2032": "15914",
    "2033": "17297",
    "2034": "18285",
    "2035": "19384",
    "2036": "20297",
    "2037": "21890",
    "2038": "23204",
    "2039": "25271",
    "2040": "26677",
    "2041": "28349",
    "2042": "29917",
    "2043": "31333",
    "2044": "32268",
    "2045": "33182",
    "2046": "33557",
    "2047": "33871",
    "2048": "33695",
    "2049": "33865",
    "2050": "33568"
  },
  {
    "Age": "85+",
    "2022": "4649",
    "2023": "4964",
    "2024": "5415",
    "2025": "5936",
    "2026": "6438",
    "2027": "7443",
    "2028": "7974",
    "2029": "8045",
    "2030": "8047",
    "2031": "8268",
    "2032": "8718",
    "2033": "9302",
    "2034": "9986",
    "2035": "10972",
    "2036": "12333",
    "2037": "13157",
    "2038": "14387",
    "2039": "15415",
    "2040": "16717",
    "2041": "18138",
    "2042": "19653",
    "2043": "21252",
    "2044": "23229",
    "2045": "24933",
    "2046": "26906",
    "2047": "28871",
    "2048": "30788",
    "2049": "32635",
    "2050": "34281"
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
