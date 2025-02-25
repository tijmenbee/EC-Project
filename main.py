import random
import matplotlib.pyplot as plt
import numpy as np
from random import getrandbits
from collections import Counter
from functions import Crossover, Fitness_CO, Fitness_TF, Gen_Pop, Crossover_List


G = 40 # Genes in individual
N = 10 # Population size

d = 2.5 # Trap Function parameter
k = 4 # Length of bit string
FitMethod = ["TF", "CO"]

ones = [1]*G
zeros = [0]*G
TransferMethod = "UX" # "UX" or "2X"


P = Gen_Pop(N,G)
Pa = P[::2]
Pb = P[1::2]


    
class genetic_algorithm():
    def __init__(self, FitMethod, TransferMethod, d = 1, blnTgtLnkd = True):
        self.k = k
        self.N = N
        self.G = G

        self.d = d
        self.FitnessMethod = FitMethod
        self.TransferMethod = TransferMethod
        self.blnTgtLnkd = blnTgtLnkd
        

        self.generation = 0
        self.highestFitness = 0
        self.countdown = 0

        self.generate_population() 
        

    def pass_fitness_function(self):
        if self.FitnessMethod == "CO":
            self.calc_fitness(Fitness_CO)
        elif self.FitnessMethod == "TF":
            self.calc_fitness(Fitness_TF,self.d,self.k,self.blnTgtLnkd)

    def calc_fitness(self, fn, *args):
        self.Fit_Pd = [fn(i, *args) for i in self.Pd]
        self.Fit_Pc = [fn(i, *args) for i in self.Pc]
        self.Fit_Pb = [fn(i, *args) for i in self.Pb]
        self.Fit_Pa = [fn(i, *args) for i in self.Pa]

    def generate_population(self): # Pa and Pb are the parents
        P = Gen_Pop(self.N, self.G)
        self.Pa = P[::2]
        self.Pb = P[1::2]
        self.Fit_Pa = [Fitness_CO(i) for i in self.Pa] 
        self.Fit_Pb = [Fitness_CO(i) for i in self.Pb]
        average_fitness = sum(self.Fit_Pa + self.Fit_Pb)/self.N
        print(f"Average fitness gen {self.generation}: {average_fitness}")
        
    def crossover(self): # Pc and Pd are the children
        self.Pc, self.Pd = Crossover_List(self.Pa, self.Pb, self.TransferMethod)
    
    def cull_population(self):
        P = []
        P_dict = {
                "d":self.Pd,
                "c":self.Pc,
                "b":self.Pb,
                "a":self.Pa
                }
        for i in range(len(self.Pa)):  # Append the highest fit values to a new array.
            dict = {
                "d":self.Fit_Pd[i],
                "c":self.Fit_Pc[i],
                "b":self.Fit_Pb[i],
                "a":self.Fit_Pa[i]
                }
        
            P.append(P_dict[max(dict, key=dict.get)][i])
            dict.pop(max(dict, key=dict.get))
            P.append(P_dict[max(dict, key=dict.get)][i])

        random.shuffle(P)
        if len(P) != self.N:
            print("Error! something went wrong with culling the population")
            exit()
        self.Pa = P[::2]
        self.Pb = P[1::2]

    def show(self):
        average_fitness = sum(self.Fit_Pa + self.Fit_Pb)/self.N
        print(f"Average fitness gen {self.generation}: {average_fitness}, Highest Fitness: {max(self.Fit_Pa + self.Fit_Pb)} ")


    def calc_end(self):
        
        tot_fit = self.Fit_Pa + self.Fit_Pb
        if G in (tot_fit):
            print(f"Global Optimum Found: {max(tot_fit)}, Generation: {self.generation}, Average Fitness: {sum(self.Fit_Pa + self.Fit_Pb)/self.N}, Population size: {self.N}")
            print(f"Specifications. Fitness method: {self.FitnessMethod}, Crossover method: {self.TransferMethod}, d value: {self.d}, is tightly linked: {self.blnTgtLnkd}")
            return True
        max_fit = max(tot_fit)
        #print(self.countdown,max_fit,self.highestFitness,max_fit > self.highestFitness)
        if max_fit > self.highestFitness:
            self.countdown = 0
            self.highestFitness = max_fit
            return False
        elif self.countdown > 19: 
            if self.N >= 1280:
                print(f"Local Optimum: {max(tot_fit)}, at N = 1280. Terminating GA")
                print(f"Specifications. Fitness method: {self.FitnessMethod}, Crossover method: {self.TransferMethod}, d value: {self.d}, is tightly linked: {self.blnTgtLnkd}")
            
                return True
            self.N = self.N*2
            print(f"Local Optimum found: {max(tot_fit)}, Restarting with N = {self.N}.")
            self.countdown = 0
            self.highestFitness = 0
            self.generation = 0
            self.generate_population()

            return False
        else: 
            self.countdown = self.countdown + 1
            return False
    def generate_graph(self):
        plt.ion()  # Turn on interactive mode
        fig, self.ax = plt.subplots()
        self.x_data, self.y_data = [], []

        # Set up the plot
        self.ax.set_xlim(0, 50)  # X-self.axis limit
        self.ax.set_ylim(0, 100)  # Y-self.axis limit
        self.line, = self.ax.plot([], [], 'b-o', label="Dynamic Data")  # Blue line with dots

        plt.xlabel("Time")
        plt.ylabel("Random Value")
        plt.title("Real-Time Dynamic Graph")
        plt.legend()

    def update_graph(self): # Not finished
        
        self.x_data.append(i)
        self.y_data.append(random.randint(0, 100))  # Generate a random value

        # Update plot data
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)
        
        # Adjust limits dynamically
        self.ax.relim()
        self.ax.autoscale_view()

        plt.draw()
        plt.pause(0.1)  # Pause for a short interval to simulate real-time update

        plt.ioff()  # Turn off interactive mode after completion
        plt.show()
    def run(self):
        while not self.calc_end():
            self.crossover()
            self.pass_fitness_function()
            self.cull_population()
            self.generation = self.generation + 1
            #self.show()

GA = genetic_algorithm("TF","2X",2.5, False)
GA.run()
        
        

TFPa_tght = [Fitness_TF(i,d,k,True) for i in P]
TFPa_lose = [Fitness_TF(i,d,k,False) for i in P]
COPa = [Fitness_CO(i) for i in P]
