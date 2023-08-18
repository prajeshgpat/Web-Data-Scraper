import requests
import re
import csv
import os

NUM_OF_ZIPCODES = 10
INDEX = "index.txt"
USZIPS = "uszips.txt"
UNFILTERED_LAT_LNGS = "./input/lat_lngs_unfiltered.csv"
FILTERED_LAT_LNGS = "heatmapdata.csv"

# Unit Tests
# UNFILTERED_LAT_LNGS = 'sample_lat_lngs_unfiltered.csv'
# FILTERED_LAT_LNGS = 'sample_lat_lngs_filtered.csv'

### Files required to run program:
"""
Input File:
index.txt Reset to 0 if new program
uszips.txt

Output files:
lat_lngs_unfiltered.csv lat_lngs_filtered.csv
"""


### Requests all stores in passed zipcode
def get_store_lat_lngs(zcode):
    lat_lngs = []
    coords = []
    request = f"https://www.starbucks.com/store-locator?place={zcode}"
    response = requests.get(request)
    coords = re.findall(
        r'"coordinates":\{"latitude":(.*?)\,"longitude":(.*?)\}', response.text
    )
    for coordinates in coords:
        lat_lngs.append((float(coordinates[1]), float(coordinates[0])))
    return lat_lngs


### Removes duplicates from list using set function
def remove_dups(all_lat_lngs: list):
    new_lat_lngs = []
    all_lat_lngs = sum(all_lat_lngs, [])
    all_lat_lngs = list(set(all_lat_lngs))
    for latlng in all_lat_lngs:
        new_lat_lngs.append(
            tuple(
                float(coord)
                for coord in latlng.replace("(", "").replace(")", "").split(", ")
            )
        )
    all_lat_lngs = new_lat_lngs
    return all_lat_lngs


### Parses through all US Zipcodes in 'uszips.csv'
def parse_zip():
    all_lat_lngs = []

    with open(USZIPS, "r") as zipcodes:
        zcodes = [zip.rstrip() for zip in zipcodes]
    zipcodes.close()

    with open(INDEX, "r") as start_index:
        stored_index = [i.rstrip() for i in start_index]
    start_index.close()

    for i in range(int(stored_index[0]), len(zcodes)):
        os.system("clear")
        print(str(i) + "/33788")

        if i % NUM_OF_ZIPCODES == 0:
            if i == 0:
                write_to_csv(UNFILTERED_LAT_LNGS, "w", all_lat_lngs, "n")
            else:
                write_to_csv(UNFILTERED_LAT_LNGS, "a", all_lat_lngs, "n")
            index = open(INDEX, "w")
            index.write(str(i))
            index.close()
            all_lat_lngs = []

        all_lat_lngs.append(get_store_lat_lngs(zcodes[i]))
    write_to_csv(UNFILTERED_LAT_LNGS, "a", all_lat_lngs, "n")
    return all_lat_lngs


### Write latitudes/longitudes to .csv
def write_to_csv(CSV_NAME: str, WRITE_MODE: str, ELEMENTS, HEADER: str):
    with open(CSV_NAME, WRITE_MODE) as f:
        write = csv.writer(f)
        if HEADER == "y":
            write.writerow(ELEMENTS)
        else:
            write.writerows(ELEMENTS)
    f.close()


### Creates csv data for google maps import
def create_csv_data(all_lat_lngs):
    rows = []
    heatmapdata = ""
    count = 0
    """
    fields = ['[']
    write_to_csv(FILTERED_LAT_LNGS, 'w', fields, 'y')
    """

    for location in all_lat_lngs:
        if location[0] < -40 and location[1] > 0:
            count += 1
            heatmapdata = (
                # "new "
                # + "google.maps.LatLng("
                # +
                "("
                + str(location[1])
                + ", "
                + str(location[0])
                + "),"
            )
            rows.append(heatmapdata)

            os.system("clear")
            print(str(count) + "/33788")
            if count == 20000:
                write_to_csv(FILTERED_LAT_LNGS, "a", rows, "n")
                count = 0
                rows = []
    with open("heatmapdata.txt", "w") as f:
        f.write("[\n")
        for line in rows:
            f.write("%s\n" % line)
        f.write("]")
    """
    write_to_csv(FILTERED_LAT_LNGS, 'a', rows, 'n')
    fields = [']']
    write_to_csv(FILTERED_LAT_LNGS, 'a', fields, 'y')
    """


def main():
    os.system("clear")
    print("BEGIN##########################################################")

    # parse_zip() #Run once you have lat_lngs_unfiltered.csv

    with open(UNFILTERED_LAT_LNGS) as csvfile:
        all_lat_lngs = [coords for coords in csv.reader(csvfile)]
    csvfile.close()

    all_lat_lngs = remove_dups(all_lat_lngs)
    create_csv_data(all_lat_lngs)

    print("END############################################################")


if __name__ == "__main__":
    main()
