import requests
import json




teste = {
  "slice":[
    {
      "slice_id":"slice1",
      "slice_part":[
        {
          "slice_part_id":"slice_part_1",
          "monitoring_agg_ip":"0.0.0.0",
          "monitoring_agg_port":"teste"
        }
      ]
    }
  ]
}

teste2 = {"slice":[]}

def edit():
  global teste2 

  print("\n")
  teste2["slice"].append({"slice_id":"slice1","monitoring_agg_ip":"0.0.0.0","monitoring_agg_port":str(99),"slice_part":[]})
  print(json.dumps(teste2))
  teste2["slice"][0]["slice_part"].append({"slice_part_id":"slice_part_2","monitoring_agg_ip":"0.0.0.0","monitoring_agg_port":"teste"})
  print(json.dumps(teste2))
  teste2["slice"].append({"slice_id":"slice2","slice_part":[]})
  print(json.dumps(teste2))
  print("\n")
  


edit()
print(json.dumps(teste2))


#print(json.dumps(teste))
#print("\n")
#teste["slice"].append({"slice_id":"slice2","slice_part":[]})
#print(json.dumps(teste))
#print("\n")
#port = 99
#teste["slice"].append({"slice_id":"slice1","monitoring_agg_ip":"0.0.0.0","monitoring_agg_port":str(port),"slice_part":[]})
#teste["slice"][0]["slice_part"].append({"slice_part_id":"slice_part_2","monitoring_agg_ip":"0.0.0.0","monitoring_agg_port":"teste"})
#print(json.dumps(teste))
#print("\n")
