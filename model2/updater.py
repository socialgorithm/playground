from multiprocessing import Process, Queue, Value

from model2.car import Car
from model2.track import Track


def updateLoop(cars_genome: list, in_queue: Queue, out_queue: Queue, ID):
    print("update process started. ID: {}".format(ID))
    cars = []
    for genome in cars_genome:
        car = Car(genome.tag, genGenome=False)
        car.setGenome(genome)
        cars.append(car)
    while True:
        item = int(in_queue.get(block=True))  # wait for main process to tell us to start
        if item > 0:
            compute_car_sensor_input(cars)
            evaluate_car_brain(cars)
            update_positions(cars)
            compute_collisions(cars)
            evaluate_fitness(cars)
            return_data(cars, out_queue)
            # DEBUG
            print("PROC_{}: loop".format(ID))
            # /DEBUG
        else:
            # kill updater
            break


def compute_car_sensor_input(cars: list):
    pass


def evaluate_car_brain(cars: list):
    pass


def update_positions(cars: list):
    pass


def compute_collisions(cars: list):
    pass


def evaluate_fitness(cars: list):
    """
    Evaluates the fitness of each car based on distance driven and on weather the car has collided etc

    :param cars:
    :return:
    """
    pass


def return_data(cars: list, out_queue: Queue):
    # creating car return dict
    return_dict = {}
    for car in cars:
        car_ret_dict = {'fitness': car.fitness, 'sensorIn': car.sensorInput, 'vector': car.vector}
        return_dict[car.tag] = car_ret_dict
    out_queue.put(return_dict, block=True)

