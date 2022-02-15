from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect()

map = vc.nc.commit_list(["MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) WHERE exists(r.accession) WITH * ORDER BY r.accession Asc, a.short_form Asc RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map"])[0]['data'][0]['row']
output = ""
for line in map[0]:
  if not line[1] in output:
    output += "\n" + "".join(line)

with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output + "\n")
