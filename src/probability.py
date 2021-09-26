import math
import random
import matplotlib.pyplot as plt

class Probability:
  """
  This class contains solvers and graphers related to probability.
  """
  @staticmethod
  def permutations(n, r):
    """
    Finds total number of arrangements of r elements from n-element set,
    which is the same as the product of the possible number of outcomes for
    each position. Algebraically, this is 'n x (n - 1) x ... x (n - r)'
    (can also be found by cancelling out (n-r)! elements from n!).
    Formula: P(n, r) = n!/(n-r)!
    """
    if r > n:
      return 0
    else:
      return math.factorial(n) / math.factorial(n - r)

  @staticmethod
  def combinations(n, r):
    """
    Finds total number of combinations (where order doesn't matter) of r
    elements from n-element set. This is found by removing duplicate
    combinations from permutations that result from different sequences of
    the same elements (ex. 1,3,2 and 2,1,3). This adds up to exactly r!.
    Example: {10,20,30,40,50} is 1 combination, but has 5x4x3x2x1 permutations
    Formula: C(n, r) = n!/(r!(n-r)!)
    """
    if r > n:
      return 0
    else:
      return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))
  
  @staticmethod
  def binomial(n, r, success_chance, r_meaning="exact"):
    """
    Finds the probability that a successful outcome happens a specific
    number of times and that a failing outcome happens the rest of the times
    in a specific number of trials. Since this only differentiates between
    successes and failures, the order does not matter.

    Formula: nCr * p^r * q^(n - r)
    
    *n=number of trials, r=number of desired outcomes, p=success chance,
    q=failure chance

    **r_meaning can be 'exact', 'min', or 'max' (ex. to find the chance of
    rolling a 1 AT MOST 2 times out of 5, call binomial(5, 2, 1/6, 'max'))
    """
    # Choose the number of successful outcomes to consider, depending on 
    # the value of 'r_meaning'
    if r_meaning == "exact":
      success_range = range(r, r + 1)
    elif r_meaning == "min":
      success_range = range(r, n + 1)
    elif r_meaning == "max":
      success_range = range(0, r + 1)

    # Add the probabilities of all acceptable numbers of successes
    total = 0
    for num_successes in success_range:
      p = success_chance ** num_successes
      q = (1 - success_chance) ** (n - num_successes)
      total += Probability.combinations(n, num_successes) * p * q
    return total

  @staticmethod
  def graph_binomial(n, r, success_chance, r_meaning="exact", trials=10, delay=0.5):
    # Set up bar graph
    fig, ax = plt.subplots()
    ax.set_ylim(0, 1)
    # Graph initial x and y values on bar graph
    successful_trials, failed_trials = 0, 0
    bar_label = ax.text(0, 0, "0")
    bars = plt.bar(["Success"], [successful_trials])
    # Graph line representing average probability
    average = Probability.binomial(n, r, success_chance, r_meaning)
    plt.axhline(y=average, linewidth=1, color='k')
    plt.text(0, average, f"Average Success: {average:.3f}")
    
    # Start filling bar graph with trial successes/failures
    for trial in range(trials):
      # Decide whether trial is a success using r and random numbers
      successful_outcomes, failed_outcomes = 0, 0
      for element in range(n):
        if random.uniform(0, 1) < success_chance:
          successful_outcomes += 1
        else:
          failed_outcomes += 1
      # Add trial success/failure to above counters
      if (r_meaning == "exact" and successful_outcomes == r or
          r_meaning == "min" and successful_outcomes >= r or
          r_meaning == "max" and successful_outcomes <= r):
        successful_trials += 1
      else:
        failed_trials += 1
      # Update the rendered graph by setting the bar heights and redrawing
      current_success = successful_trials / (successful_trials + failed_trials)
      bars[0].set_height(current_success)
      bar_label.set_position((0, current_success / 2))
      bar_label.set_text(f"{current_success:.3f}")
      fig.canvas.draw()
      # Pause for 0.5 seconds between trials
      plt.pause(delay)
    plt.show()