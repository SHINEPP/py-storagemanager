import geoip2.database

if __name__ == '__main__':
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    db_type = reader.metadata().database_type
    print(f'Country.mmdb db_type: {db_type}')

    response = reader.city('38.54.106.207')
    print(f'Country.mmdb response: {response}')
