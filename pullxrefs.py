from vfb_connect.cross_server_tools import VfbConnect
import os

# Check if file exists and count initial lines
initial_lines = 0
if os.path.exists('neuronbridge.map'):
    with open('neuronbridge.map', 'r') as file:
        initial_lines = sum(1 for line in file)
print(f"Initial number of lines in neuronbridge.map: {initial_lines}")

vc = VfbConnect()

# Query for matches with non-empty accession filter
query = """
MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) 
WHERE exists(r.accession) AND r.accession[0] <> ''
WITH * 
ORDER BY r.accession Asc, a.short_form Desc 
RETURN DISTINCT collect({ 
    accession: r.accession[0],
    destination: a.short_form
}) as map
"""

print("\nProcessing matches...")
results = vc.nc.commit_list([query])[0]['data'][0]['row']
print(f"Number of unique matches found in query: {len(results[0])}")

output = ""
exact_count = 0
wildcard_count = 0

# Process each unique accession-destination pair
for entry in results[0]:
    # Skip if accession is empty
    if not entry['accession']:
        continue
        
    # Add exact match
    exact_line = f'    rewrite "^/xref/neuronbridge/{entry["accession"]}" "https://v2.virtualflybrain.org/reports/{entry["destination"]}" last;'
    output += "\n" + exact_line
    exact_count += 1
    
    # Add wildcard match
    wildcard_line = f'    rewrite "^/xref/neuronbridge/(.*):{entry["accession"]}" "https://v2.virtualflybrain.org/reports/{entry["destination"]}" last;'
    output += "\n" + wildcard_line
    wildcard_count += 1

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
print(f"Wildcard match lines added: {wildcard_count}")
print(f"Final lines in file: {final_lines}")

# Print a sample of the final content
print("\nSample of final content (first 6 lines to show both patterns):")
with open('neuronbridge.map', 'r') as file:
    for i, line in enumerate(file):
        if i < 6:
            print(line.strip())
