import urllib.request
import json

url = 'https://overpass-api.de/api/interpreter'
query = """
[out:json];
(
  way["building"](18.055,83.400,18.065,83.412);
  node["amenity"](18.055,83.400,18.065,83.412);
  node["building"](18.055,83.400,18.065,83.412);
);
out center;
"""

req = urllib.request.Request(url, data=query.encode(), method='POST')
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())

print(f"Found {len(result.get('elements', []))} elements\n")
for e in result.get('elements', []):
    tags = e.get('tags', {})
    name = tags.get('name', tags.get('amenity', tags.get('building', 'unnamed')))
    if e.get('center'):
        lat = e['center']['lat']
        lon = e['center']['lon']
    else:
        lat = e.get('lat', 'N/A')
        lon = e.get('lon', 'N/A')
    print(f"{name} | lat={lat}, lon={lon} | tags={json.dumps(tags)}")
