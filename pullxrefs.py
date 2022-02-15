from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect()

map = vc.nc.commit_list(["MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) WHERE exists(r.accession) RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map"])[0]['data'][0]['row']
output = ""
for line in map:
  output += "/n" + "".join(line)

print(output)
