###########################
## EARTH MOVER'S PROBLEM ##
###########################
import numpy as np
import math
import plotly.express as px 


# INITIALIZATION

# Create Point 
# each point has an x and y coord and a color
class point:
    # Initializes a point using the x and y coordinate as input parameters
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "none"
        self.partner = None
        self.paired = False

        # Hungarian ALgorithm Stuff
        self.scanned = False
        self.label = None
        # used if point is red
        self.u =  math.inf # min weight on edges in the complete bipartite graph
        # used if point is blue
        self.v = math.inf
        self.p = 0
    
    # Set the color of a point
    def setColor(self, color):
        self.color = color

    # Checks to see if two points are pairable
    def match(self, other):
        if (self.color == "red" or self.color =="blue") and (other.color == "red" or other.color == "blue"):
            if self.color != other.color:
                return True
            else:
                return False
        else:
            return False

    # Pairs two points to each other. Updates both objects
    def pair(self, other):
        self.paired = True
        other.paired = True
        self.partner = other
        other.partner = self

    # Prints info about a specific point
    def display_info(self):
        print(f"Coord: ({self.x}, {self.y})\nColor: {self.color}\n" )
    

# Initialize a problem space where max is the max coordinate size 
# and n is the number of points 
def initPoints(max, n):
    if n > max*max:
        raise ValueError("n too high for max")
    if n%2==1:
        raise ValueError("n must be even")
    
    # Create a list of initialized coords
    takenCoords = []
    points = []

    # randomly place n points
    numPoints = 0
    while numPoints < n:
        x = np.random.randint(max)
        y = np.random.randint(max)
        if (x,y) not in takenCoords:
            takenCoords.append((x,y))
            points.append(point(x,y))
            numPoints += 1
    return points

# PARTITION FUNCTIONS
# These are different methods to partition the list of points
# These always return equal sized lists of red points and blue points

# partition random
def partitionRand(points):
    n = len(points)
    np.random.shuffle(points)
    for i in range(int(n/2)):
        points[i].setColor("red")
    for i in range(int(n/2), n):
        points[i].setColor("blue")

    return points[:int(n/2)], points[int(n/2):]

# partition algorithm 


# EARTH MOVER'S DISTANCE USING HUNGARIAN ALGORITHM

# Find Point Distance 
def pointDist(point1, point2):
    return math.sqrt(float(point1.x - point2.x)**2 + float(point1.y - point2.y)**2)

# Set u's
def setU(reds, blues):
    for red in reds:
        min_u = math.inf
        for blue in blues:
            cand_u = pointDist(red, blue)
            if cand_u < min_u:
                min_u = cand_u
                red.u = min_u

# Hungarian Algorithm Implementation
def matchPoints(reds, blues):
    # Step 0
    setU(reds, blues)
    X = [] # set of tuples 

    ####################
    # STEP 1: Labeling #
    ####################
    # 1.0 Give the label "null" to each exposed point in reds

    # 1.1 if no unscanned labels OR if there are unscanned labels, but each 
    # unscanned label is on a node i in blues for which p<math.inf, then go to step 3 


    # 1.2 Find a point i with an unscanned label, where 
    # if i in reds:
    #   go to step 1.3
    # elif (i in blues) AND (blue.p == math.inf)
    #   go to step 1.4


    # 1.3 Scan the label on point i (i in reds) as follows
    #  
    # For each edge (red, blue) not in X incident to point i
    #   if red.u + blue.u - pointDist(red, blue) > blue.p:
    #       blue.label = "i"
    #       blue.p = red.u + blue.u - pointDist(red, blue) 
    # return to step 1.1


    # 1.4 Scan the label on point i (i in blue) as follows
    # 
    # If node i is exposed:
    #   go to step 2
    # else
    #   identify the unique edge (red, blue) in X incident to point blue and label red "i" 
    # return to step 1.1

    ########################
    # STEP 2: AUGMENTATION #
    ########################
    # An augmenting path has been found, terminating at point i, identified in 
    # Step 1.2) The points preceding point i in the path are identified by 
    # "backtracking" from label to label. Augment X by adding to X all edges 
    # not in X and removing from X those which are. Set blue.p equal to 0 for 
    # each point in blues. Remove all labels from points. Return to step 1.0

    ####################################
    # STEP 3: CHANGE IN DUAL VARIABLES #
    ####################################
    

#def matchPoints(reds, blues):
#    minDist = math.inf
#    matchPoint = None
#    for red in reds:
#        for blue in blues:
#            # if the blue is not yet paired
#            if not blue.paired:
#                dist = pointDist(red,blue)
#                if dist < minDist:
#                    minDist = dist
#                    matchPoint = blue
#        red.pair(blue)
#    return reds




# EMDistance

# you start with the complete bipartite graph with each edge being weighted by the distance
# you then remove points to find a minimized matching
def EMD(reds):
    sum = 0
    for red in reds:
        sum += pointDist(red, red.partner)
    return sum

# Pipeline
def pipeline(max, n): #TODO: Update this to also let you choose which partition algoirthm to choose
    # Initialize points
    points = initPoints(max, n)
    
    # Partition
    reds, blues = partitionRand(points)

    # Match Points
    matchPoints(reds, blues)

    # EMD
    return(EMD(reds))

def main():
    data = []
    for i in range(100):
        data.append(pipeline(100, 100))
    fig = px.histogram(data)
    fig.show()
        
        



# return EMD


if __name__ == '__main__':
    main()