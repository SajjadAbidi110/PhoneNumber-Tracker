import os
import phonenumbers
from phonenumbers import geocoder,carrier
from opencage.geocoder import OpenCageGeocode
import folium

number = input("Enter Number: ")
def pointer(lat,lng):
    map_location = folium.Map(location=[lat,lng],zoom_start=10)
    folium.Marker([lat,lng],popup='Location').add_to(map_location)

    map_loc = "location.html"
    map_location.save(map_loc)

    os.system(f"open {map_loc}")


check_number = phonenumbers.parse(number)
location_of_number = geocoder.description_for_number(check_number,'en')
print(f'Location: {location_of_number}')

sim_carrier = carrier.name_for_number(check_number,'en')
if sim_carrier != '':
    print(f"Carrier:{sim_carrier}")

key = "8f0a081dc3644ec0b0c30167460e3086"
geocoder_api = OpenCageGeocode(key)

result = geocoder_api.geocode(location_of_number)

if result:
    latitude = result[0]['geometry']['lat']
    longitude = result[0]['geometry']['lng']

    reverse = geocoder_api.reverse_geocode(latitude,longitude)
    components = reverse[0]['components']
    if reverse:
        city = components.get('city') or components.get('town') or components.get('village')

        if city:
            print(f"City = {city}")
            city_result = geocoder_api.geocode(city)
            city_lat = city_result[0]['geometry']['lat']
            city_lng = city_result[0]['geometry']['lng']
            print(f"City Coordinates = {city_lat},{city_lng}")
            pointer(city_lat,city_lng)

        else:
            print(f"Coordinates of country = {latitude},{longitude}")
            pointer(latitude,longitude)
    else:
        print("City not found")
else:
    print("Location not found")
