from itertools import permutations
import json
f = open("level1b.json")
data = json.load(f)

length1=data["n_neighbourhoods"]
length2=data["n_restaurants"]
length=length1+length2
adj_mat=[]

for i in range(0,data["n_restaurants"]):
    row_cost=[]
    for j in range(0,length):
        if(i>=j):
            row_cost.append(data["restaurants"]["r0"]["restaurant_distance"][i])
        else:
            row_cost.append(data["restaurants"]["r0"]["neighbourhood_distance"][j-1])
    adj_mat.append(row_cost)

for i in range(0,length1):
    row_cost=[]
    for j in range(0,length):
        if(j==0):
            row_cost.append(data["restaurants"]["r0"]["neighbourhood_distance"][i])
        else:
            row_cost.append(data["neighbourhoods"]["n{}".format(i)]["distances"][j-1])
    adj_mat.append(row_cost)

demand=[]
for i in data["neighbourhoods"]:
    demand.append(data["neighbourhoods"][i]["order_quantity"])

max_cap=data["vehicles"]["v0"]["capacity"]

f.close()

def tsp_nearest_neighbor(adjacency_matrix,cap,dem):
   
    unvisited = set(range(length))
    tour = []
    ptour=[]
    mcap=cap
    # Start from the first city
    current_city = 0
    tour.append(current_city)
    unvisited.remove(current_city)

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: adjacency_matrix[current_city][city])
        tour.append(nearest_city)
        if(demand[nearest_city-1]<=cap):
            cap=cap-demand[nearest_city-1]    
            unvisited.remove(nearest_city)
            current_city = nearest_city
        else:
            cap=mcap
            tour.remove(nearest_city)
            tour.append(0)
            ptour.append(tour)
            tour=[]
            unvisited.add(0)
            current_city=0

    # Return to the starting city to complete the tour
    tour.append(0)
    ptour.append(tour)
    return ptour

path_num=tsp_nearest_neighbor(adj_mat,max_cap,demand)
print(path_num)
path_string=[]
for i in path_num:
    string=[]
    for j in range(len(i)):
        if(i[j]==0):
            string.append("r0")
        else:
            s="n"+str(i[j]-1)
            string.append(s)
    path_string.append(string)
print(path_string)
f1=open("level1b_Output.json","w")
data1={"v0":{"path1":path_string[0],"path2":path_string[1],"path3":path_string[2],"path4":path_string[3]}}
json.dump(data1,f1)
