Genetic Algorithm for majority gate optimization  

Version 1.0 Results  

Successfully produces the following  
AND  
OR  
XOR  
HA  
FA  


Comparisons for solution generation time between GA and random search.   
Neither used multiprocessing.   

XOR - averaged over 100 solutions  
GA: 20.007s  
Random: 33.421s  

HA - averaged over 10 solutions  
GA: 228.544s   
Random Search: 237.911s



Version 2.0 Results

Measured time and total number of circuits searched for each method
Ideally the genetic algorithm should search fewer circuits to get a correct answer

XOR - averaged over 10 solutions
GA: 1.421 s
average circuits searched: 20,900
Random Search: 1.3s
average circuits searched: 39,050

HA - averaged over 10 solutions
GA: 0.683s, 6980 circuits searched 
Random Search: 12.72s, 173,581 circuits searched

FA - average time to find a solution (10 trials)
GA: 8.304 s, 62,300 circuits searched
Random Search: searched over 40 millions circuits so I just killed it

Not sure why random search was much faster in v2.0 compared to v1.0.
Might be due to random generation being faster.

V2.0 definitely proves GA is better than random search. most likely due to improved breeding and better fitness function
