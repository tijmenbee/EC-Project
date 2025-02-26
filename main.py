import random
import matplotlib.pyplot as plt
import numpy as np
import time
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
        #print(f"Average fitness gen {self.generation}: {average_fitness}")
        
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

    # Check if the algorithm is progressing
    def is_progressing(self, tot_fit,):
        max_fit = max(tot_fit)

        if max_fit > self.highestFitness:
            self.countdown = 0  
            self.highestFitness = max_fit  
            return True  

        self.countdown += 1  

        if self.countdown > 19:  
            #print("No progress detected for 20 generations. Checking termination conditions.")
            return False  

        return True  

    # Bisection search for optimal population size
    def bisection_search(self):
        low, high = self.N // 2, self.N  
        best_N = high
        
        while high - low >= 10: # Search until the range is less than 10
            print(low, high)
            mid = (low + high) // 2
            mid = round(mid / 10) * 10  # Ensure population size is a multiple of 10
            self.N = mid
            successful_runs = 0

            # Run the GA 10 times for this population size
            for _ in range(10):
                self.generate_population()
                self.highestFitness = 0
                self.generation = 0
                tot_fit = self.Fit_Pa + self.Fit_Pb

                # Run the GA until it stops progressing
                while self.is_progressing(tot_fit):
                    self.crossover()
                    self.pass_fitness_function()
                    self.cull_population()
                    self.generation += 1
                    tot_fit = self.Fit_Pa + self.Fit_Pb

                # Check if the GA found the optimal solution, then increment the counter
                if G in tot_fit:  
                    successful_runs += 1

            print(f"Population Size: {mid}, Successful Runs: {successful_runs}/10")
            
            if successful_runs >= 9:  
                best_N = mid  
                high = mid  
            else:
                low = mid + 1

        self.N = best_N  
        
    # Check if the termination condition is met
    def calc_end(self):
        
        tot_fit = self.Fit_Pa + self.Fit_Pb
        if G in (tot_fit):
            self.successful_runs += 1  
            return True
        max_fit = max(tot_fit)
        #print(self.countdown,max_fit,self.highestFitness,max_fit > self.highestFitness)
        # Check if the algorithm is progressing
        if max_fit > self.highestFitness:
            self.countdown = 0
            self.highestFitness = max_fit
            return False
        elif self.countdown > 19: 
            self.countdown = 0
            self.highestFitness = 0
            self.generation = 0
            self.generate_population()
            return True
        else: 
            self.countdown = self.countdown + 1
            return False
    
    
    def run(self):
        self.successful_runs = 0
        self.run_count = 0 

        # Keep running until either the population size exceeds 1280 or the optimal solution is found
        while True:
            self.generate_population()
            self.highestFitness = 0
            self.generation = 0

            # Run the GA until it stops progressing
            while not self.calc_end():
                self.crossover()
                self.pass_fitness_function()
                self.cull_population()
                self.generation += 1
            
            self.run_count += 1  # Count each run

            if self.run_count >= 10:  # After 10 runs, decide what to do
                print(f"Population Size: {self.N}, Successful Runs: {self.successful_runs}/10")

                if self.successful_runs >= 9:  # If 9 or more were successful, proceed to bisection
                    self.bisection_search()
                    return  

                # Otherwise, double the population and reset counters
                self.N *= 2
                if self.N > 1280:
                    print("Population size exceeded 1280. Terminating.")            
                    return False
                print(f"Not enough successful runs. Increasing population to N = {self.N}. Restarting 10 runs.")
                self.successful_runs = 0  
                self.run_count = 0
        
        
    
GA = genetic_algorithm("CO", "2X", 2.5, True)
GA.run()
            

TFPa_tght = [Fitness_TF(i,d,k,True) for i in P]
TFPa_lose = [Fitness_TF(i,d,k,False) for i in P]
COPa = [Fitness_CO(i) for i in P]
