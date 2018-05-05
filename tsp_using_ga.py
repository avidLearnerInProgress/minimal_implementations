import random
import time
import numpy
import copy
import matplotlib.pyplot as plt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #   STEP 1  #       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Determining Values of:
#      -    Chromosomes.
#      -    Generations.
#      -    Mutation Rate.
#      -    Crossover Rate.
#

#   Adjust these to problem.
#   Please Keep Cities and Chromosomes > 1
TotalCities = 5
Chromosomes = 3
TotalGenerations = 4
CrossOverRate = 0.25
MutationRate = 0.1

Generation = 0

#   If a gene is below this number, it shall mutate.
MutationNumber = int((TotalCities * Chromosomes) * MutationRate)

#   Total Score of Generation
Total = 0

#   Coordinates of each City goes here.
Cities = []

#   Travel Costs between each city goes here.
TravelCost = []
#   Total Cost of each path goes here.
PathScore = []
#   Fitness of each Chromosome.
Fitness = []
#   Probability of each Chromosome, reproducing.
Probability = []
#   Cumulative probability values / Roulette wheel.
Roulette = []
#   Random Possibilities to Select from Roulette.
RandomPossibilities = []
#   New Generation's Path Values
NewPath = []
#   This boolean is used for automatically refreshing Plot diagram.
#   Making this True means solution was found, so diagram should NOT be
#   interactive anymore.
NotInteractivePlot = False
#   Best Score
BestScore = 0

print ''
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Welcome to Travelling Salesman Problem.'
print 'Algorithm used: Genetic.'
print 'Provided solution for #' + str(TotalCities) + ' cities.'
print 'Number of Chromosomes: ' + str(Chromosomes)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Each city has a (x,y) position.'
print 'Each city has a Travel cost.'
print 'You can travel between any given city.'
print ''

#   Random Values between [0, TotalCities]. Returns Int Array.
def InitializePath():
    Temp = []

    for x in range(Chromosomes):
        AppendList = [i for i in range(TotalCities)]
        random.shuffle(AppendList)
        Temp.append(AppendList)

    return Temp

#   Calculates Score of Each Path. Returns Int Array.
def CalcPathScore(Path):
    Temp = []

    for x in range(Chromosomes):

        print 'Path used: ' + str(Path[x])

        #   Using this as a starting value, so i dont have to use modulo inside the loop.
        #   it's basically the cost between last and first city. (Return to Homelands).

        Score = TravelCost[Path[x][TotalCities - 1]][Path[x][0]]

        #   Calculating all Costs between selected path.
        #   Adding them to a final score and printing it
        for i in range(TotalCities - 1):
            Score += TravelCost[Path[x][i]][Path[x][i + 1]]

            print 'Cost from #' + str(Path[x][i]) + ' to #' + str(Path[x][i + 1]) + ' is: ' + \
                  str(TravelCost[Path[x][i]][Path[x][i + 1]])

        # Printing Return to Home.
        print 'Cost from #' + str(Path[x][TotalCities - 1]) + ' to #' + str(Path[x][0]) + ' is: ' + \
              str(TravelCost[Path[x][TotalCities - 1]][Path[x][0]])

        Temp.append(Score)
        print 'Final Path Score: ' + str(Temp[x]) + '\n'
        time.sleep(0.5)

    return Temp

#   This Function Creates the City Connection Graph.
#   Parameters: Path -  Fittest Path of Generation should be given.
#               Index - Index of Fittest Path.
#               PathScore - Score of Fittest Path
def PlotCities(Path, index, PathScore):

    #   Clear existing figure.
    fig = plt.gcf()
    fig.clf()

    #   All lines below, prepare the ground for plotting.
    plt.subplot(1,2,1)
    plt.title('Cities: ' + str(TotalCities) + '    Path ' + str(index+1) +' of ' + str(Chromosomes) + '    Score: ' + str(PathScore[index]), fontsize='10')
    fig.canvas.set_window_title('Gen # ' + str(Generation) + ' - City Connection Graph')
    plt.ion()

    if (NotInteractivePlot):
        plt.ioff()

    plt.xlabel('X')
    plt.ylabel('Y')

    #   These are the plot arrays. Make them null every time this function is called.
    #   They get appended below.
    #   And finally plotted afterwards.
    x = []
    y = []

    #   This loop, 'decodes' Path values.
    #   For example if Path is 0->2->1, it starts appending x and y.
    #   final x,y should look like this:
    #   x[0] = City #0 x location, y[0] = City #0 y location.
    #   x[1] = City #2 x location, y[1] = City #2 y location.
    #   x[2] = City #1 x location, y[2] = City #1 y location.
    #   Appending one more time after loop ends, so i got the 'Return to Home' Path.
    #   x[3] = City #0 x location, y[3] = City #0 y location.

    for i in range(TotalCities):
        curCity = Path[index][i]
        x.append(Cities[curCity][0])
        y.append(Cities[curCity][1])

        #   Adding Labels to Data Points.
        plt.text(Cities[curCity][0], Cities[curCity][1], '  City ' + str(curCity))

    x.append(Cities[Path[index][0]][0])
    y.append(Cities[Path[index][0]][1])

    #   Finally Plotting.
    plt.plot(x, y, '-r*')

    #   Preparing the Ground for Roulette Pie Chart.
    plt.subplot(1, 2, 2)
    plt.title('Roulette')

    #   number of slices must match number of Chromosomes.
    #   Copying PathScore to a new list.
    #   Getting Indexes of Max Value in Pathscore, so roulette
    #   Shows Paths Correctly.
    #   HAVE TO DO THIS because Pie Chart automatically sets values to highest scores
    #   and Path Indexes are not displayed correctly if let to default.
    name_list = copy.copy(PathScore)
    Labels = []
    for x in range(Chromosomes):
        index = name_list.index(max(name_list))
        Labels.append(index)
        name_list[index] = 0

    labels = ['Path #' + str(x) for x in Labels]

    #   Transposing Array from (n,1) to (1,n).
    TpathScore = copy.copy(PathScore)
    numpy.transpose(TpathScore)


    #   MORE COLORS, append this with hex values.

    Colors = [  '#990033', '#7B9C3B', '#AB8BEC',
                '#B6B6B4', '#9C3B3B', '#5B3B9C',
                '#4863A0', '#1F45FC', '#C6DEFF',
                '#3B9C9C'
             ]


    #   Plotting Pie Chart
    patches, texts = plt.pie(TpathScore, shadow=False, startangle=0, colors=Colors,)
    plt.legend(patches, labels, bbox_to_anchor=(1,0))
    plt.axis('equal')
    for w in patches:
        w.set_linewidth(1.3)
        w.set_edgecolor('black')

    #   Use this for better Visuals.
    plt.tight_layout()

    #   Displaying to user and pausing it, so user can take notice of it.
    plt.show()
    plt.pause(1)

#   Calculating Fitness of each Path. Returns Float Array.
#   Formula Used:   1 / (1 + PathScore[x]).
def CalcFitness(PathScore):
    Temp = []

    for x in range(Chromosomes):
        Temp.append(float(1 / float((1 + PathScore[x]))))

    return Temp


#   Adds Up all Fitness Scores. Returns Int.
def CalcTotal(Fitness):

    Total = 0

    for x in range(Chromosomes):
        Total += Fitness[x]

    return Total

#   Calculates Probability of each Chromosome being reproduced based on its Fitness Score.
#   More Fit == More Chances. Returns Float Array.
def CalcProbabilities(Fitness, Total):
    Temp = []

    for x in range(Chromosomes):
        Temp.append(float(Fitness[x] / Total))

    return Temp

#   Calculates Roulette Wheel. Value of last element MUST be 1.0. Returns Float Array.
def CalcRoulette(Probability):
    a = 0.0
    Temp = []

    for x in range(Chromosomes):
        a += Probability[x]
        Temp.append(a)

    return Temp

#   Generates New Path based on Random Selected Chromosomes. Returns Int Array[Chromosomes][TotalCities]
def CalcNewPath(Path, Roulette, RandomPossibilities):

    NewPath = InitializePath()

    for x in range(Chromosomes):
        for i in range(Chromosomes):
            if RandomPossibilities[x] < Roulette[i]:
                NewPath[x] = Path[i]
                break

    return NewPath

#   Crossover-ing Paths may cause duplicates to appear.
#   Use this to fix that.
#   Returns Int Array.
def FixPaths(Path):
    Temp = copy.copy(Path)
    print 'Mutated Path:\t' + str(Temp)
    for i in range(Chromosomes):
        notSeen = []
        duplicates = []
        for x in range(len(Temp[i])):
            if x not in Temp[i]:
                notSeen.append(x)

            else:
                if Temp[i].count(x) > 1:

                    #   If Found more than 2 times, need to append accordingly.
                    for j in range(1, Temp[i].count(x)):
                        duplicates.append(x)

        for x in range(len(duplicates)):
            index = Temp[i].index(duplicates[x])
            Temp[i][index] = notSeen[x]

    print 'Fixing path..'
    time.sleep(0.5)
    print 'Path Fixed. New Path:\t' + str(Temp) + '\n'
    return Temp

#   Mutation Happens here. Use MutationNumber = Chromosomes*TotalCities / MutationRate.
#   If cell value is lower than that, replace it with a random in range(0,TotalCities-1)
#   Calls Above function to fix generated path.
def Mutation(Path):
    Temp = copy.copy(Path)
    for x in range(Chromosomes):
        for i in range(TotalCities):
            if (Temp[x][i] <= MutationNumber):
                Temp[x][i] = random.randint(0,TotalCities-1)

    Temp = FixPaths(Temp)
    return Temp


def Crossover(Path):
    #   Chances of each Path are stored here.
    RandomCrossRate = [random.uniform(0.0, 1.0) for x in range(Chromosomes)]

    #   Ensures that there are at least 2 parents in each generation.
    #   Doing this to avoid out of index error.
    RandomCrossRate[0] = CrossOverRate
    RandomCrossRate[1] = CrossOverRate

    SelectedPaths = []
    Temp = []

    #   If Chance of Path is > 25%, Appending SelectedPaths list with that path and making that position ZERO.
    #   I do this, to recognise afterwards which positions were selected.
    for x in range(Chromosomes):
        if (RandomCrossRate[x] >= CrossOverRate):
            SelectedPaths.append(Path[x])
            Path[x] = [0]

    #   Positions of slices.
    RandomPositions = [random.randint(1, TotalCities - 1) for x in range(len(SelectedPaths))]

    #   Slicing to random positions. Repeating for last element outside loop.
    #   Using Temp List to store Temp data.
    for x in range(len(SelectedPaths) - 1):
        a = SelectedPaths[x][:RandomPositions[x] + 1] + SelectedPaths[x + 1][RandomPositions[x] + 1:]
        Temp.append(a)

    a = SelectedPaths[len(SelectedPaths) - 1][:RandomPositions[len(SelectedPaths) - 1] + 1] + SelectedPaths[0][
                                                                                              RandomPositions[len(
                                                                                                  SelectedPaths) - 1] + 1:]
    Temp.append(a)

    #   Reversing Temp list, so 1st element goes to bottom.
    #   I can use pop() function to insert Generated Path to First occurrence of Zero.
    Temp.reverse()

    for x in range(Chromosomes):
        if (Path[x] == [0]):
            Path[x] = Temp.pop()

    print 'Crossovered Path:\t' + str(Path)

    Path = Mutation(Path)
    return Path


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #   STEP 2  #       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   -   Initializing City Values : Choosing (x,y) for each city, looping for # of cities.
#   -   Initializing Travel Costs : Choosing random cost values [0,10]
#


for x in range(TotalCities):
    #   City's Coordinates are created here. Appending Cities list each time this loops.
    #   Value Range is [0-100].
    #   Same for TravelCost, but then it's divided by 10 to keep them in [0-10] range.
    #   Could do range(10), but it wouldn't run for more than 10 cities.
    Cities.append(random.sample(range(100), 2))
    TravelCost.append(random.sample(range(100), TotalCities))

    #   Line Below Divides each number that was assigned above by 10.
    #   This makes sure that more than 10 and less that 100 cities can be given.
    #   Program should run for [1-99] number of cities.
    TravelCost[x][:] = [y / 10 for y in TravelCost[x]]

    #  Cost Travelling between same City must be 0. Therefore, sum of TravelCost Diagonal should be 0.
    TravelCost[x][x] = 0

    #   Printing each City and its Travel Cost.
    print 'City #' + str(x) + '\tCoordinates: ' + str(Cities[x]) + ',\tTravel Cost: ' + str(TravelCost[x])


print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #####################       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #   STEP 4,5,6,7,8  #       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #####################       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   -   4. Evaluation of fitness value of chromosomes by calculating objective function
#   -   5. Chromosomes selection
#   -   6. Crossover
#   -   7. Mutation

#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 0 GEN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print 'CURRENT GENERATION: 0'

#   Saving values of Best Path and each Index in Paths/ NewPaths Arrays for printing at the very end.
TempIndex = 0
BestPath = []
BestScorePath = []

#   Initializes first Set of Paths.
Path = InitializePath()

#   Calculating Score of each Path.
PathScore = CalcPathScore(Path)

#   Calculating Fitness of each Path.
#   Formula Used:   1 / (1 + PathScore[x]).
Fitness = CalcFitness(PathScore)

#   Adds All fitness elements of array above.
Total = CalcTotal(Fitness)

#   Probability of each chromosome by reproduced.
#   Formula used:   Fitness[x] / Total
Probability = CalcProbabilities(Fitness, Total)

#   Calculate Roulette Wheel.
#   Last element of this Array should be 1.0
#   Use this Array to Select new Generation of Chromosomes.
Roulette = CalcRoulette(Probability)

#   Returns Random Float Array in range (0.0, 1.0).
#   Use this Array in combination with Roulette Array, to select random Chromosomes for new generation.
RandomPossibilities = [random.uniform(0.0, 1.0) for x in range(Chromosomes)]



#   Grabbing index of shortest path, this is generation 0, so it is more like an initialization.
TempIndex = PathScore.index(min(PathScore))

#   Showing to user current generation's Shortest path.
PlotCities(Path, TempIndex, PathScore)


BestPath = copy.copy(Path)
BestScore = min(PathScore)

BestScorePath = copy.copy(PathScore)



#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 0 GEN ENDS HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #   STEP 3  #       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   -   Process steps 4-7 until the number of generations is met
#


for x in range(1,TotalGenerations + 1):
    print ''
    print 'CURRENT GENERATION: ' + str(x)
    NewPath = CalcNewPath(Path, Roulette, RandomPossibilities)

    NewPath = Crossover(NewPath)

    PathScore = CalcPathScore(NewPath)

    if (min(PathScore) < BestScore):
        Generation = x
        BestScore = min(PathScore)
        BestPath = []
        BestPath = copy.copy(NewPath)
        BestScorePath = []
        BestScorePath = copy.copy(PathScore)

        TempIndex = PathScore.index(min(PathScore))
        PlotCities(NewPath, TempIndex, PathScore)

    #   Mutation of Paths is happening first, so i have to loop one more time than total Generations.
    #   Need to stop creating new paths when that happens.
    #   Keeping PathScore outside, just to display scores of last Gen.

    if (x < TotalGenerations):
        Fitness = CalcFitness(PathScore)
        Total = CalcTotal(Fitness)
        Probability = CalcProbabilities(Fitness, Total)
        Roulette = CalcRoulette(Probability)
        RandomPossibilities = [random.uniform(0.0, 1.0) for x in range(Chromosomes)]



#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #   STEP 8  #       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     #############       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   -   Solution (Best Chromosomes)
#

print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Program Finished.'
print 'Fittest Gen: ' + str(Generation)
NotInteractivePlot = True
print 'Fittest Path Found: ' + str(BestPath[TempIndex])
print 'Scoring:\t' + str(BestScore)
PlotCities(BestPath, TempIndex, BestScorePath)
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'