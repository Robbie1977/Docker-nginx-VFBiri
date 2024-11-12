from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect()

# Function to extract ID from accession
def get_base_id(accession):
    """Extract the base ID from an accession string by finding the last numeric part."""
    return accession.split(':')[-1]

# Query for neuronbridge exact mappings
neuronbridge_exact_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect(
    '    rewrite ^/xref/' + b.short_form + '/' + r.accession + 
    ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;'
) as map
"""

# Query for neuronbridge regex mappings
neuronbridge_regex_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH *, get_base_id(r.accession) as base_id
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect(
    '    rewrite ^/xref/' + b.short_form + '/([^:]+:)+' + base_id + 
    ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;'
) as map
"""

# Query for jrc_slide_code_api mappings
jrc_query = """
MATCH (a)-[r]->(b:Site {short_form:'jrc_slide_code_api'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect(
    '    rewrite ^/xref/' + b.short_form + '/' + r.accession + 
    ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;'
) as map
"""

# Generate mappings
output = ""

# Process neuronbridge exact mappings first
map = vc.nc.commit_list([neuronbridge_exact_query])[0]['data'][0]['row']
for line in map[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))

# Process neuronbridge regex mappings second
map = vc.nc.commit_list([neuronbridge_regex_query])[0]['data'][0]['row']
for line in map[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))

# Process jrc_slide_code_api mappings
map = vc.nc.commit_list([jrc_query])[0]['data'][0]['row']
for line in map[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))

# Write to file
with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output.strip() + "\n")
