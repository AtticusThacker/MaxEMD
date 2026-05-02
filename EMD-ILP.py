"""
The Beer Distribution Problem with Extension for A Competitor Supply Node for the PuLP Modeller
"""

# Import PuLP modeler functions
from pulp import *
import csv

def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**1/2

# Creates a list of all the supply nodes
# set1 = ["A", "B", "C"]
# set1_points = {"A": [0,1], "B": [0,2], "C": [0,3]}

# # Creates a dictionary for the number of units of supply for each supply node
# supply = {"A": 1, "B": 1, "C": 1}

# # Creates a list of all demand nodes
# set2 = ["1", "2", "3"]#, "4", "5"]
# set2_points = {"1": [1, 0], "2": [2,0], "3": [3,0], "4": [4,0], "5": [5,0]}

# # Creates a dictionary for the number of units of demand for each demand node
# demand = {
#     "1": 1,
#     "2": 1,
#     "3": 1,
#     "4": 1,
#     "5": 1,
# }



def load_points(filename):
    """
    Reads a CSV file with fields:
    type,id,x,y,units

    Returns:
        set1 (list of supply node names)
        set1_points (dict: id -> [x, y])
        supply (dict: id -> units)

        set2 (list of demand node names)
        set2_points (dict: id -> [x, y])
        demand (dict: id -> units)
    """

    set1 = []
    set1_points = {}
    supply = {}

    set2 = []
    set2_points = {}
    demand = {}

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_type = row["type"].strip().lower()
            node_id = row["id"]
            x = float(row["x"])
            y = float(row["y"])
            units = float(row["units"])

            if node_type == "supply":
                set1.append(node_id)
                set1_points[node_id] = [x, y]
                supply[node_id] = units

            elif node_type == "demand":
                set2.append(node_id)
                set2_points[node_id] = [x, y]
                demand[node_id] = units

            else:
                raise ValueError(f"Unknown type '{row['type']}' in row: {row}")

    return set1, set1_points, supply, set2, set2_points, demand

# =========================================
# start main
# =========================================

set1 = []
set1_points = {}
supply = {}

set2 = []
set2_points = {}
demand = {}

set1, set1_points, supply, set2, set2_points, demand = load_points("test.csv")

# Creates a list of costs of each transportation path
costs = []

for i in set1:
    row = []
    for j in set2:
        row.append(dist(set1_points[i],set2_points[j]))
    costs.append(row)

# The cost data is made into a dictionary
costs_dict = makeDict([set1, set2], costs, 0)

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("EMD", LpMinimize)

# Creates a list of tuples containing all the possible routes for transport
Routes = [(i, j) for i in set1 for j in set2]

# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
vars = LpVariable.dicts("Route", (set1, set2), 0, None, LpInteger)

# The objective function is added to 'prob' first
prob += (
    lpSum([vars[w][b] * costs_dict[w][b] for (w, b) in Routes]),
    "Sum_of_Transporting_Costs",
)

# The supply maximum constraints are added to prob for each supply node (warehouse)
for i in set1:
    prob += (
        lpSum([vars[i][j] for j in set2]) <= supply[i],
        f"Sum_of_Products_out_of_Warehouse_{i}",
    )

# The demand minimum constraints are added to prob for each demand node (bar)
for j in set2:
    prob += (
        lpSum([vars[i][j] for i in set1]) >= demand[j],
        f"Sum_of_Products_into_Bar{j}",
    )

# The problem data is written to an .lp file
prob.writeLP("BeerDistributionProblem.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Transportation = ", value(prob.objective))
