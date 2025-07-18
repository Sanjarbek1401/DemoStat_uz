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
    "2022": "2939700",
    "2023": "2984402",
    "2024": "3028045",
    "2025": "3070235",
    "2026": "3111112",
    "2027": "3150580",
    "2028": "3188585",
    "2029": "3225319",
    "2030": "3260615",
    "2031": "3294365",
    "2032": "3326367",
    "2033": "3356510",
    "2034": "3384742",
    "2035": "3410864",
    "2036": "3435130",
    "2037": "3457514",
    "2038": "3478341",
    "2039": "3497767",
    "2040": "3516078",
    "2041": "3533660",
    "2042": "3551011",
    "2043": "3568471",
    "2044": "3586191",
    "2045": "3604284",
    "2046": "3622912",
    "2047": "3642039",
    "2048": "3661610",
    "2049": "3681561",
    "2050": "3701756"
  },
  {
    "Age": "0-4",
    "2022": "297362",
    "2023": "315423",
    "2024": "328385",
    "2025": "336047",
    "2026": "340322",
    "2027": "338994",
    "2028": "336207",
    "2029": "332798",
    "2030": "329071",
    "2031": "324838",
    "2032": "320034",
    "2033": "314659",
    "2034": "308469",
    "2035": "301451",
    "2036": "294009",
    "2037": "286376",
    "2038": "278996",
    "2039": "272104",
    "2040": "266201",
    "2041": "261419",
    "2042": "258231",
    "2043": "256664",
    "2044": "256704",
    "2045": "258171",
    "2046": "260849",
    "2047": "264230",
    "2048": "267918",
    "2049": "271709",
    "2050": "275369"
  },
  {
    "Age": "5-9",
    "2022": "264158",
    "2023": "263626",
    "2024": "267055",
    "2025": "272282",
    "2026": "279701",
    "2027": "293729",
    "2028": "311161",
    "2029": "323645",
    "2030": "331036",
    "2031": "335223",
    "2032": "333970",
    "2033": "331347",
    "2034": "328133",
    "2035": "324619",
    "2036": "320615",
    "2037": "316060",
    "2038": "310954",
    "2039": "305058",
    "2040": "298360",
    "2041": "291257",
    "2042": "283972",
    "2043": "276936",
    "2044": "270369",
    "2045": "264761",
    "2046": "260229",
    "2047": "257235",
    "2048": "255802",
    "2049": "255919",
    "2050": "257411"
  },
  {
    "Age": "10-14",
    "2022": "259853",
    "2023": "259884",
    "2024": "258792",
    "2025": "257425",
    "2026": "259725",
    "2027": "261577",
    "2028": "260984",
    "2029": "264309",
    "2030": "269363",
    "2031": "276522",
    "2032": "290163",
    "2033": "307167",
    "2034": "319337",
    "2035": "326564",
    "2036": "330717",
    "2037": "329544",
    "2038": "327061",
    "2039": "324006",
    "2040": "320664",
    "2041": "316850",
    "2042": "312507",
    "2043": "307637",
    "2044": "302003",
    "2045": "295586",
    "2046": "288774",
    "2047": "281777",
    "2048": "275013",
    "2049": "268695",
    "2050": "263302"
  },
  {
    "Age": "15-19",
    "2022": "211370",
    "2023": "219697",
    "2024": "231739",
    "2025": "242093",
    "2026": "251232",
    "2027": "256679",
    "2028": "256597",
    "2029": "255504",
    "2030": "254183",
    "2031": "256501",
    "2032": "258356",
    "2033": "257766",
    "2034": "261037",
    "2035": "265998",
    "2036": "273008",
    "2037": "286364",
    "2038": "302980",
    "2039": "314824",
    "2040": "321862",
    "2041": "325949",
    "2042": "324844",
    "2043": "322513",
    "2044": "319637",
    "2045": "316488",
    "2046": "312876",
    "2047": "308743",
    "2048": "304092",
    "2049": "298684",
    "2050": "292506"
  },
  {
    "Age": "20-24",
    "2022": "207787",
    "2023": "202170",
    "2024": "198635",
    "2025": "202443",
    "2026": "204960",
    "2027": "209873",
    "2028": "217627",
    "2029": "228932",
    "2030": "238533",
    "2031": "246917",
    "2032": "251836",
    "2033": "251690",
    "2034": "250874",
    "2035": "249899",
    "2036": "252345",
    "2037": "254159",
    "2038": "253514",
    "2039": "256722",
    "2040": "261617",
    "2041": "268387",
    "2042": "281037",
    "2043": "296615",
    "2044": "307585",
    "2045": "314122",
    "2046": "318068",
    "2047": "317176",
    "2048": "315243",
    "2049": "312800",
    "2050": "310082"
  },
  {
    "Age": "25-29",
    "2022": "248390",
    "2023": "242580",
    "2024": "235785",
    "2025": "227220",
    "2026": "216482",
    "2027": "207837",
    "2028": "202976",
    "2029": "199803",
    "2030": "203536",
    "2031": "205820",
    "2032": "210340",
    "2033": "217341",
    "2034": "227643",
    "2035": "236299",
    "2036": "244002",
    "2037": "248662",
    "2038": "248662",
    "2039": "248137",
    "2040": "247342",
    "2041": "249799",
    "2042": "251711",
    "2043": "251286",
    "2044": "254531",
    "2045": "259182",
    "2046": "265373",
    "2047": "277008",
    "2048": "291422",
    "2049": "301545",
    "2050": "307655"
  },
  {
    "Age": "30-34",
    "2022": "267691",
    "2023": "263797",
    "2024": "258514",
    "2025": "252826",
    "2026": "249008",
    "2027": "242785",
    "2028": "237554",
    "2029": "231502",
    "2030": "223890",
    "2031": "214220",
    "2032": "206485",
    "2033": "202257",
    "2034": "199385",
    "2035": "203067",
    "2036": "205180",
    "2037": "209388",
    "2038": "215824",
    "2039": "225398",
    "2040": "233398",
    "2041": "240642",
    "2042": "245146",
    "2043": "245301",
    "2044": "245054",
    "2045": "244485",
    "2046": "247047",
    "2047": "249089",
    "2048": "248817",
    "2049": "252027",
    "2050": "256440"
  },
  {
    "Age": "35-39",
    "2022": "237199",
    "2023": "247111",
    "2024": "253825",
    "2025": "257865",
    "2026": "258945",
    "2027": "258114",
    "2028": "254424",
    "2029": "249572",
    "2030": "244387",
    "2031": "241078",
    "2032": "235439",
    "2033": "230825",
    "2034": "225450",
    "2035": "218641",
    "2036": "209839",
    "2037": "202824",
    "2038": "199081",
    "2039": "196432",
    "2040": "200066",
    "2041": "202056",
    "2042": "206060",
    "2043": "212115",
    "2044": "221186",
    "2045": "228737",
    "2046": "235672",
    "2047": "240089",
    "2048": "240379",
    "2049": "240331",
    "2050": "239896"
  },
  {
    "Age": "40-44",
    "2022": "187811",
    "2023": "195469",
    "2024": "200647",
    "2025": "208623",
    "2026": "218464",
    "2027": "229061",
    "2028": "238251",
    "2029": "244498",
    "2030": "248323",
    "2031": "249393",
    "2032": "248734",
    "2033": "245393",
    "2034": "240998",
    "2035": "236263",
    "2036": "233351",
    "2037": "228144",
    "2038": "223979",
    "2039": "219104",
    "2040": "212884",
    "2041": "204722",
    "2042": "198238",
    "2043": "194867",
    "2044": "192420",
    "2045": "196056",
    "2046": "198007",
    "2047": "201892",
    "2048": "207678",
    "2049": "216367",
    "2050": "223567"
  },
  {
    "Age": "45-49",
    "2022": "160936",
    "2023": "162723",
    "2024": "169350",
    "2025": "174458",
    "2026": "177845",
    "2027": "182156",
    "2028": "189400",
    "2029": "194231",
    "2030": "201783",
    "2031": "211122",
    "2032": "221206",
    "2033": "229978",
    "2034": "235962",
    "2035": "239683",
    "2036": "240789",
    "2037": "240292",
    "2038": "237232",
    "2039": "233187",
    "2040": "228803",
    "2041": "226208",
    "2042": "221361",
    "2043": "217567",
    "2044": "213092",
    "2045": "207337",
    "2046": "199693",
    "2047": "193640",
    "2048": "190571",
    "2049": "188287",
    "2050": "191913"
  },
  {
    "Age": "50-54",
    "2022": "147731",
    "2023": "149411",
    "2024": "149767",
    "2025": "152191",
    "2026": "154515",
    "2027": "155311",
    "2028": "156971",
    "2029": "163310",
    "2030": "168172",
    "2031": "171407",
    "2032": "175531",
    "2033": "182486",
    "2034": "187101",
    "2035": "194337",
    "2036": "203276",
    "2037": "212931",
    "2038": "221346",
    "2039": "227101",
    "2040": "230730",
    "2041": "231878",
    "2042": "231548",
    "2043": "228773",
    "2044": "225071",
    "2045": "221035",
    "2046": "218749",
    "2047": "214251",
    "2048": "210788",
    "2049": "206649",
    "2050": "201275"
  },
  {
    "Age": "55-59",
    "2022": "143611",
    "2023": "141333",
    "2024": "139500",
    "2025": "136973",
    "2026": "137842",
    "2027": "140582",
    "2028": "142165",
    "2029": "142489",
    "2030": "144804",
    "2031": "147063",
    "2032": "147917",
    "2033": "149542",
    "2034": "155627",
    "2035": "160270",
    "2036": "163391",
    "2037": "167350",
    "2038": "174002",
    "2039": "178425",
    "2040": "185341",
    "2041": "193870",
    "2042": "203086",
    "2043": "211141",
    "2044": "216668",
    "2045": "220220",
    "2046": "221438",
    "2047": "221310",
    "2048": "218844",
    "2049": "215492",
    "2050": "211811"
  },
  {
    "Age": "60-64",
    "2022": "123475",
    "2023": "127992",
    "2024": "130407",
    "2025": "132744",
    "2026": "132893",
    "2027": "131997",
    "2028": "129981",
    "2029": "128449",
    "2030": "126237",
    "2031": "127187",
    "2032": "129855",
    "2033": "131405",
    "2034": "131770",
    "2035": "133996",
    "2036": "136214",
    "2037": "137179",
    "2038": "138791",
    "2039": "144574",
    "2040": "148964",
    "2041": "151967",
    "2042": "155752",
    "2043": "162047",
    "2044": "166284",
    "2045": "172848",
    "2046": "180915",
    "2047": "189619",
    "2048": "197239",
    "2049": "202474",
    "2050": "205900"
  },
  {
    "Age": "65-69",
    "2022": "82967",
    "2023": "87153",
    "2024": "93931",
    "2025": "98459",
    "2026": "103113",
    "2027": "108084",
    "2028": "112092",
    "2029": "114305",
    "2030": "116477",
    "2031": "116741",
    "2032": "116166",
    "2033": "114592",
    "2034": "113501",
    "2035": "111740",
    "2036": "112825",
    "2037": "115427",
    "2038": "116967",
    "2039": "117419",
    "2040": "119560",
    "2041": "121742",
    "2042": "122852",
    "2043": "124473",
    "2044": "129904",
    "2045": "134026",
    "2046": "136918",
    "2047": "140519",
    "2048": "146388",
    "2049": "150410",
    "2050": "156530"
  },
  {
    "Age": "70-74",
    "2022": "51568",
    "2023": "55608",
    "2024": "58523",
    "2025": "61634",
    "2026": "64161",
    "2027": "68498",
    "2028": "72048",
    "2029": "77795",
    "2030": "81649",
    "2031": "85685",
    "2032": "90001",
    "2033": "93546",
    "2034": "95627",
    "2035": "97674",
    "2036": "98116",
    "2037": "97908",
    "2038": "96826",
    "2039": "96205",
    "2040": "94936",
    "2041": "96139",
    "2042": "98646",
    "2043": "100173",
    "2044": "100739",
    "2045": "102780",
    "2046": "104913",
    "2047": "106169",
    "2048": "107785",
    "2049": "112769",
    "2050": "116549"
  },
  {
    "Age": "75-79",
    "2022": "24552",
    "2023": "25551",
    "2024": "28093",
    "2025": "31979",
    "2026": "36474",
    "2027": "38692",
    "2028": "41853",
    "2029": "44098",
    "2030": "46605",
    "2031": "48741",
    "2032": "52218",
    "2033": "55154",
    "2034": "59806",
    "2035": "62973",
    "2036": "66355",
    "2037": "69960",
    "2038": "72987",
    "2039": "74910",
    "2040": "76772",
    "2041": "77359",
    "2042": "77503",
    "2043": "76923",
    "2044": "76768",
    "2045": "76019",
    "2046": "77315",
    "2047": "79673",
    "2048": "81136",
    "2049": "81785",
    "2050": "83635"
  },
  {
    "Age": "80-84",
    "2022": "16518",
    "2023": "17716",
    "2024": "17289",
    "2025": "16466",
    "2026": "16145",
    "2027": "15736",
    "2028": "16599",
    "2029": "18346",
    "2030": "20955",
    "2031": "24042",
    "2032": "25558",
    "2033": "27826",
    "2034": "29432",
    "2035": "31315",
    "2036": "33016",
    "2037": "35584",
    "2038": "37844",
    "2039": "41307",
    "2040": "43714",
    "2041": "46336",
    "2042": "49123",
    "2043": "51525",
    "2044": "53189",
    "2045": "54777",
    "2046": "55456",
    "2047": "55873",
    "2048": "55730",
    "2049": "55948",
    "2050": "55655"
  },
  {
    "Age": "85+",
    "2022": "6721",
    "2023": "7159",
    "2024": "7809",
    "2025": "8506",
    "2026": "9285",
    "2027": "10884",
    "2028": "11695",
    "2029": "11731",
    "2030": "11612",
    "2031": "11865",
    "2032": "12557",
    "2033": "13536",
    "2034": "14589",
    "2035": "16074",
    "2036": "18081",
    "2037": "19362",
    "2038": "21296",
    "2039": "22857",
    "2040": "24866",
    "2041": "27081",
    "2042": "29392",
    "2043": "31916",
    "2044": "34988",
    "2045": "37654",
    "2046": "40619",
    "2047": "43745",
    "2048": "46765",
    "2049": "49668",
    "2050": "52258"
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
StatisticsData.objects.filter(region=tashkent_city_region, gender='jami').delete()

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
                    gender='jami',
                    population=population
                )

print("Navoi female data import completed successfully!")
