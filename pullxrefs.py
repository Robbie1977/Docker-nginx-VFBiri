from vfb_connect.cross_server_tools import VfbConnect
import os

# Check if file exists and count initial lines
initial_lines = 0
if os.path.exists('neuronbridge.map'):
    with open('neuronbridge.map', 'r') as file:
        initial_lines = sum(1 for line in file)
print(f"Initial number of lines in neuronbridge.map: {initial_lines}")

vc = VfbConnect()

# Query for exact matches
exact_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map
"""

# Get exact match results and count
print("\nProcessing exact matches...")
exact_results = vc.nc.commit_list([exact_query])[0]['data'][0]['row']
print(f"Number of exact matches found in query: {len(exact_results[0])}")

# Generate mappings
output = ""

# Add exact matches first
exact_added = 0
for line in exact_results[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))
        exact_added += 1
print(f"Number of unique exact matches added: {exact_added}")

# Query for wildcard matches
wildcard_query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/(.*):' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map
"""

# Get wildcard match results and count
print("\nProcessing wildcard matches...")
wildcard_results = vc.nc.commit_list([wildcard_query])[0]['data'][0]['row']
print(f"Number of wildcard matches found in query: {len(wildcard_results[0])}")

# Add wildcard matches
wildcard_added = 0
for line in wildcard_results[0]:
    if not line[1].replace(" ","%20") in output:
        output += "\n" + "".join(line).replace(line[1], line[1].replace(" ","%20"))
        wildcard_added += 1
print(f"Number of unique wildcard matches added: {wildcard_added}")

# Write to file
with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output.strip() + "\n")

# Count final lines
with open('neuronbridge.map', 'r') as file:
    final_lines = sum(1 for line in file)

print("\nSummary:")
print(f"Initial lines in file: {initial_lines}")
print(f"Exact matches found: {len(exact_results[0])}")
print(f"Unique exact matches added: {exact_added}")
print(f"Wildcard matches found: {len(wildcard_results[0])}")
print(f"Unique wildcard matches added: {wildcard_added}")
print(f"Final lines in file: {final_lines}")
