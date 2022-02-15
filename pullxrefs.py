from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect()

map = vc.nc.commit_list(["MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) WHERE exists(r.accession) WITH * ORDER BY r.accession Asc, a.short_form Desc RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map"])[0]['data'][0]['row']
output = ""
for line.replace(" ","%20") in map[0]:
  if not line[1] in output:
    output += "\n" + "".join(line).replace(line[1],line[1].replace(" ","%20"))

map = vc.nc.commit_list(["MATCH (a)-[r]->(b:Site {short_form:'jrc_slide_code_api'}) WHERE exists(r.accession) WITH * ORDER BY r.accession Asc, a.short_form Desc RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map"])[0]['data'][0]['row']
for line.replace(" ","%20") in map[0]:
  if not line[1] in output:
    output += "\n" + "".join(line).replace(line[1],line[1].replace(" ","%20"))
    
with open('neuronbridge.map', 'w') as the_file:
    the_file.write(output + "\n")
    
