from vfb_connect.cross_server_tools import VfbConnect
import os

# Check if file exists and count initial lines
initial_lines = 0
if os.path.exists('neuronbridge.map'):
    with open('neuronbridge.map', 'r') as file:
        initial_lines = sum(1 for line in file)
print(f"Initial number of lines in neuronbridge.map: {initial_lines}")

vc = VfbConnect(endpoint='http://kb.virtualflybrain.org', usr='neo4j', pwd='vfb')

# Updated query to handle both accession formats
query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) 
AND r.accession[0] <> ''
AND NOT a:Deprecated
WITH a, r, 
CASE 
    WHEN r.accession[0] CONTAINS ':' 
    THEN LAST(SPLIT(r.accession[0], ':'))
    ELSE r.accession[0]
END as body_id,
r.accession[0] as full_accession
ORDER BY r.accession ASC, a.short_form DESC 
RETURN DISTINCT collect({ 
    accession: r.accession[0],
    body_id: body_id,
    destination: a.short_form
}) as map
"""

print("\nProcessing matches...")
results = vc.nc.commit_list([query])[0]['data'][0]['row']
print(f"Number of unique matches found in query: {len(results[0])}")

output = ""
exact_count = 0
body_id_count = 0
version_wildcard_count = 0

# Process each unique accession-destination pair
for entry in results[0]:
    if not entry['accession']:
        continue
        
    # Add exact match for full accession
    exact_line = f'    rewrite "^/xref/neuronbridge/{entry["accession"]}" "https://v2.virtualflybrain.org/reports/{entry["destination"]}" last;'
    output += "\n" + exact_line
    exact_count += 1
    
    # If accession contains dataset_name (has colon)
    if ':' in entry['accession']:
        # Add match for body_id only
        body_id_line = f'    rewrite "^/xref/neuronbridge/{entry["body_id"]}" "https://v2.virtualflybrain.org/reports/{entry["destination"]}" last;'
        output += "\n" + body_id_line
        body_id_count += 1
        
        # Add match for dataset_name:VERSION:body_id pattern
        dataset_name = entry['accession'].split(':')[0]
        version_wildcard_line = f'    rewrite "^/xref/neuronbridge/{dataset_name}:.*:{entry["body_id"]}" "https://v2.virtualflybrain.org/reports/{entry["destination"]}" last;'
        output += "\n" + version_wildcard_line
        version_wildcard_count += 1

# Write to file
with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output.strip() + "\n")

# Count final lines
with open('neuronbridge.map', 'r') as file:
    final_lines = sum(1 for line in file)

print("\nSummary:")
print(f"Initial lines in file: {initial_lines}")
print(f"Unique matches found: {len(results[0])}")
print(f"Exact match lines added: {exact_count}")
print(f"Body ID match lines added: {body_id_count}")
print(f"Version wildcard match lines added: {version_wildcard_count}")
print(f"Final lines in file: {final_lines}")

# Print a sample of the final content
print("\nSample of final content (first 9 lines to show all patterns):")
with open('neuronbridge.map', 'r') as file:
    for i, line in enumerate(file):
        if i < 9:
            print(line.strip())
