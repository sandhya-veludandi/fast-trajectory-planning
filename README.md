# Part 6: Statistical Hypothesis Test
If we were to compare the performance differences between Repeated Forward A* Smallest G and Adaptive A*, we would measure the average run time.
Our null hypothesis would be that there is no difference between the average run time of Repeated Forward A* Smallest G and Adaptive A*: avg(Repeated Forward A* Smallest G) == avg(Adaptive A*). 
Then, our alternative hypothesis would be that there is a performance difference between the search algorithms. 
Our method to get the average run times would to generate 100 random mazes, and then find the Repeated Forward A* Smallest G and the Adaptive A* runtime. Then, we would find the average runtime for each algorithm, and find the p-value. If the p-value is less than 0.05 then we will reject the null hypothesis that there is no performance difference between the 2 algorithms and accept the alternative hypothesis that there is a performance difference between Repeated Forward A* Smallest G and Adatpive A*. 


# How to Run Project
1, 2, 3, 4 correspond to 
adaptiveA, backwardA, forwardA largestG, forward smallestG searches

In the terminal, run
```
python maze.py [number] .\testcases\testcase[number]
```
For example, 
To run adaptiveA on testcase1:
```
python maze.py 1 .\testcases\testcase1
```
# Optimal Testcase Results
### Testcase1
![testcaset1](img_results/testcase-optimal-img-results/testcase1-optimal-img-results.png)

### Testcase2
![testcaset2](img_results/testcase-optimal-img-results/testcase2-optimal-img-results.png)

### Testcase3
![testcaset3](img_results/testcase-optimal-img-results/testcase3-optimal-img-results.png)

### Testcase4
![testcaset4](img_results/testcase-optimal-img-results/testcase4-optimal-img-results.png)

### Testcase5
![testcaset5](img_results/testcase-optimal-img-results/testcase5-optimal-img-results.png)

# All Search Testcases vs. Optimal Testcases

# AdaptiveA vs. Optimal

# BackwardA vs. Optimal 

# ForwardA Largest G vs. Optimal

# ForwardA Smallest G vs. Optimal
