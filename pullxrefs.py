from vfb_connect.cross_server_tools import VfbConnect
vc = VfbConnect(neo_endpoint="http://pdb.v4.virtualflybrain.org", neo_credentials=('neo4j','vfb'))

map = vc.nc.commit_list(["MATCH (a)-[r]->(b:Site {short_form:'neuronbridge'}) WHERE exists(r.accession) RETURN DISTINCT collect( '    rewrite ^/xref/' + b.short_form + '/' + r.accession + ' https://v2.virtualflybrain.org/reports/' + a.short_form + ' last;') as map"])[0]['data'][0]['row'][0]

print(map)
