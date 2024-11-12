from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect()

# Query for exact matches
exact_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map
"""

# Query for wildcard matches
wildcard_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/(.*):' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map
"""

# Generate mappings
output = ""

# Add exact matches first
map = vc.nc.commit_list([exact_query])[0]['data'][0]['row']
for line in map[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))

# Add wildcard matches second
map = vc.nc.commit_list([wildcard_query])[0]['data'][0]['row']
for line in map[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))

# Write to file
with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output + "\n")
