# Probability
## Subsets
### Permutations
`Probability.permutations(n, r)` returns the number of permutations (arrangements) of r elements from n-sized sets, where order does matter.
```
print(Probability.permutations(7, 4))
>>> 840
```

### Combinations
`Probability.combinations(n, r)` returns the number of combinations of r elements from n-sized sets, where order does not matter.
```
print(Probability.combinations(5, 3))
>>> 10
```

## Chance
### Binomial
`Probability.binomial(n, r, success_chance, r_meaning="exact")` finds the probability of a successful outcome happening a specific number of times and a failing outcome happening the rest of the times in a specific number of trials.
- n is the total number of trials
- r is the desired number of successes
- success_chance is the chance of a successful outcome happening
- r_meaning decides how the number of successful outcomes should compare to r. The value of r_meaning can be either 'exact', 'min', or 'max'. For example, if r_meaning is 'min', then this calculates the chance that a successful outcome happens AT LEAST r times.
```
print(Probability.binomial(6, 3, 0.6, r_meaning="max"))
>>> 0.456
```

## Graphs
### Binomial Graph
`Probability.graph_binomial(n, r, success_chance, r_meaning="exact", trials=10, delay=0.5)` runs actual trials of binomial probability and graphs their successes on a bar graph. Alongside this bar graph, the calculated binomial probability will be graphed as a horizontal line as a reference point.
- n, r, success_chance, and r_meaning are the same as in `Probability.binomial()`
- trials is the number of n-sized sets you want to test
- delay is the amount of time (in seconds) between trials
```
Probability.graph_binomial(6, 3, 0.6, r_meaning="max", trials=15, delay=0.25)
```
![Binomial Graph](/docs/images/probability_binomial.JPG)