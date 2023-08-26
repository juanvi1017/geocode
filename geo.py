import googlemaps
import requests
from dotenv import load_dotenv
import os
load_dotenv()


if __name__ == '__main__':
    # Params connection and consultation
    nameNeighbor = ''
    iteration = 0
    addressNumber = 1300
    address = ' SE Stark St, Portland, OR 97214'
    args = {
        'timeRelation': 'esriTimeRelationOverlaps',
        'geometry': '',
        'geometryType': 'esriGeometryPoint',
        'inSR': '4326',
        'spatialRel': 'esriSpatialRelIntersects',
        'units': 'esriSRUnit_Foot',
        'outFields': '*',
        'returnGeometry': 'false',
        'featureEncoding': 'esriDefault',
        'f': 'json'
    }

    def geocode():
        global iteration
        global addressNumber
        global address
        global nameNeighbor
        global args

        if iteration > 0:
            addressNumber = addressNumber + 100
            iteration = iteration + 1

        #Autentication API KEY
        gmaps = googlemaps.Client(key=os.environ.get("KEY"))

        try:
            # Geocoding an address
            geocode_result = gmaps.geocode(str(addressNumber) + address)
            result = geocode_result[0]['geometry']['location']
            if result:
                args['geometry'] = str(result['lng']) + \
                                       ', ' + str(result['lat'])

            response = requests.get(os.environ.get("URLGEO"), params=args) #Consultation endpoint ArcGIS REST
            if response.status_code == 200:
                data = response.json()
                if len(nameNeighbor) < 1:
                    iteration += 1
                    nameNeighbor = data['features'][0]['attributes']['NAME']
                    print('Vecindario localizado ' + nameNeighbor)
                    geocode()
                else:
                    if data['features'][0]['attributes']['NAME'] == nameNeighbor:
                        print('IGUAL ' + nameNeighbor)
                        geocode()
                    else:
                        print('DIFERENTE')
                        print(str(addressNumber) + address)
                        print(args['geometry'])
                        print(data['features'][0]['attributes']['NAME'])
            else:
                print('Error consulta API')
        except:
            print("An exception occurred")

    geocode()


    # ADJUNTE ARCHIVO .ENV
