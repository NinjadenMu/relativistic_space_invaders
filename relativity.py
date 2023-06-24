import math


def combined_velocity_parallel(velocity1, velocity2):
    return (velocity1 + velocity2) / (1 + velocity1 * velocity2) 


def combined_velocity_perpendicular(velocity1, velocity2):
    return math.sqrt(velocity1 ** 2 + velocity2 ** 2 - velocity1 ** 2 * velocity2 ** 2)


def gamma(combined_velocity):
    return 1 / math.sqrt(1 - combined_velocity ** 2)
