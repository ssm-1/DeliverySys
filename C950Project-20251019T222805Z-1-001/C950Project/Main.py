import csv
import datetime
from datetime import timedelta
import Truck  # Import the Truck module
from Truck import DeliveryTruck  # Import the DeliveryTruck class from the Truck module
from HashTableCreation import HashMapCreation  # Import the HashMapCreation class for hash table operations
from Package import Parcel  # Import the Parcel class for package data
import re  # Import the regex module for parsing weights

# Initialize the distance matrix
distance_matrix = {}

def load_distance_data(filepath):
    """
    Loads distance data from a CSV file into the distance matrix.

    Args:
        filepath (str): The path to the CSV file containing distance data.
    """
    global distance_matrix
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 3:
                print(f"Skipping invalid row: {row}")
                continue
            try:
                location1, location2, distance = row
                if location1 not in distance_matrix:
                    distance_matrix[location1] = {}
                distance_matrix[location1][location2] = float(distance)
            except ValueError as e:
                print(f"Error processing row {row}: {e}")

def read_csv_data(filepath):
    """
    Reads data from a CSV file and returns it as a list of rows.

    Args:
        filepath (str): The path to the CSV file to be read.

    Returns:
        list: A list of rows from the CSV file.
    """
    with open(filepath, newline='', encoding='utf-8-sig') as csv_file:
        return list(csv.reader(csv_file))

def load_address_data(filepath):
    """
    Loads address data from a CSV file and returns it as a list.

    Args:
        filepath (str): The path to the CSV file containing address data.

    Returns:
        list: A list of address data where each entry is a row from the CSV.
    """
    address_list = []
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            address_list.append(row)
    return address_list

def parse_weight(weight_str):
    """
    Parses a weight string and converts it to a float.

    Args:
        weight_str (str): The weight string to be parsed (e.g., '88 Kilos').

    Returns:
        float: The weight value as a float.
    """
    weight_str = weight_str.strip().replace('Kilos', '').replace(' ', '')
    try:
        return float(weight_str)
    except ValueError:
        print(f"Error converting weight '{weight_str}' to float.")
        return 0.0

def populate_package_data(csv_file, hash_table):
    """
    Populates a hash table with package data from a CSV file.

    Args:
        csv_file (str): The path to the CSV file containing package data.
        hash_table (HashMapCreation): The hash table object to populate with package data.
    """
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for entry in reader:
            try:
                pkg_id = int(entry[0])
                pkg_address = entry[1]
                pkg_city = entry[2]
                pkg_state = entry[3]
                pkg_zip = entry[4]
                pkg_deadline = entry[5]
                pkg_weight = parse_weight(entry[6])
                pkg_status = "At Hub"

                parcel = Parcel(pkg_id, pkg_address, pkg_city, pkg_state, pkg_zip, pkg_deadline, pkg_weight, pkg_status)
                hash_table.insert(pkg_id, parcel)
            except ValueError as e:
                print(f"Error processing row {entry}: {e}")

def get_distance_between(location1, location2):
    """
    Calculates the distance between two locations using a distance matrix.

    Args:
        location1 (str): The name of the first location.
        location2 (str): The name of the second location.

    Returns:
        float: The distance between the two locations, or inf if not found.
    """
    try:
        return distance_matrix.get(location1, {}).get(location2, float('inf'))
    except Exception as e:
        print(f"Error finding distance between {location1} and {location2}: {e}")
        return float('inf')

def find_address_id(text_address):
    """
    Finds the address ID from the address list based on a given address.

    Args:
        text_address (str): The address to search for.

    Returns:
        int: The ID of the address if found.

    Raises:
        ValueError: If the address cannot be located in the address list.
    """
    for entry in address_list:
        if text_address in entry[1]:
            return int(entry[0])
    raise ValueError(f"Address '{text_address}' could not be located")

def update_package_address_if_needed(current_time, hash_table):
    """
    Updates the delivery address of a package if the current time is past a defined update time.

    Args:
        current_time (timedelta): The current time to check against the update time.
        hash_table (HashMapCreation): The hash table containing package data.
    """
    update_time = timedelta(hours=10, minutes=20)
    if current_time >= update_time:
        package = hash_table.lookup(9)
        if package:
            new_address = "410 S State St, Salt Lake City, UT, 84103"
            package.delivery_address = new_address
            hash_table.insert(package.get_id(), package)

def get_user_time():
    """
    Prompts the user to enter the current time and returns it as a timedelta object.

    Returns:
        timedelta: The current time entered by the user as a timedelta object.
    """
    user_input = input("Please enter the time (HH:MM:SS): ").strip()
    try:
        parsed_time = datetime.datetime.strptime(user_input, "%H:%M:%S").time()
        return timedelta(hours=parsed_time.hour, minutes=parsed_time.minute, seconds=parsed_time.second)
    except ValueError:
        print("Invalid time format. Please enter time in HH:MM:SS format.")
        return None

def schedule_deliveries(truck):
    """
    Schedules deliveries for a truck based on the packages it carries and their delivery addresses.

    Args:
        truck (DeliveryTruck): The truck object that needs to schedule deliveries.
    """
    update_time = timedelta(hours=10, minutes=20)
    package_id = 9
    package = hash_table.lookup(package_id)
    if truck.current_time >= update_time and package:
        new_address = "410 S State St"
        package.delivery_address = new_address
        hash_table.insert(package.get_id(), package)

    pending_deliveries = [hash_table.lookup(parcel_id) for parcel_id in truck.package_ids]
    truck.package_ids.clear()

    while pending_deliveries:
        min_distance = float('inf')
        nearest_parcel = None
        for parcel in pending_deliveries:
            if parcel is None:
                continue
            try:
                dist = get_distance_between(truck.current_location, parcel.delivery_address)
                if dist < min_distance:
                    min_distance = dist
                    nearest_parcel = parcel
            except ValueError as e:
                print(e)

        if nearest_parcel:
            truck.package_ids.append(nearest_parcel.parcel_id)
            pending_deliveries.remove(nearest_parcel)
            truck.total_mileage += min_distance
            truck.current_location = nearest_parcel.delivery_address
            travel_time = timedelta(hours=min_distance / truck.travel_speed)
            truck.current_time += travel_time
            nearest_parcel.delivery_time = truck.current_time
            nearest_parcel.departure_time = truck.departure_time

# Load address data from a CSV file
address_list = load_address_data('CSV/Addresses.csv')

# Load distance data from a CSV file
load_distance_data('CSV/Distances.csv')

# Create instances of DeliveryTruck with example data
truck1 = Truck.DeliveryTruck(max_capacity=16, travel_speed=18, current_load=0.0,
                             package_ids=[1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], total_mileage=0.0,
                             current_location="4001 South 700 East", departure_time=timedelta(hours=8))
truck2 = Truck.DeliveryTruck(max_capacity=16, travel_speed=18, current_load=0.0,
                             package_ids=[3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 33, 35, 36, 38, 39],
                             total_mileage=0.0, current_location="4001 South 700 East", departure_time=timedelta(hours=8))
truck3 = Truck.DeliveryTruck(max_capacity=16, travel_speed=18, current_load=0.0,
                             package_ids=[4, 7, 8, 9, 10, 11, 26, 32], total_mileage=0.0,
                             current_location="4001 South 700 East", departure_time=timedelta(hours=9))

# Create a hash table to store package information
hash_table = HashMapCreation()

# Populate package data into the hash table
populate_package_data("CSV/Packages.csv", hash_table)

# Schedule deliveries for each truck
schedule_deliveries(truck1)
schedule_deliveries(truck2)
truck3.departure_time = min(truck1.current_time, truck2.current_time)
schedule_deliveries(truck3)

# User interface for interacting with the delivery system
class UserInterface:
    def __init__(self):
        print("Welcome to the Parcel Delivery System")
        self.display_combined_mileage()
        self.user_command()

    def display_combined_mileage(self):
        """
        Displays the combined mileage for all trucks.
        """
        combined_mileage = truck1.total_mileage + truck2.total_mileage + truck3.total_mileage
        print(f"Combined mileage for all trucks: {combined_mileage:.2f} miles")

    def user_command(self):
        """
        Handles user commands and interacts with the user.
        """
        while True:
            user_command = input("Enter 'time' to continue or 'exit' to terminate: ").strip().lower()
            if user_command == "time":
                self.handle_time()
            elif user_command == "exit":
                print("Exiting the system.")
                break
            else:
                print("Unknown Command. Please enter 'time' or 'exit'.")

    def handle_time(self):
        """
        Handles the 'time' command, prompting the user for the current time and package status queries.
        """
        current_time = get_user_time()
        if current_time is not None:
            status_query = input("Type 'solo' for one package status or 'all' for status of all packages: ").strip().lower()
            if status_query == "solo":
                self.handle_solo_query(current_time)
            elif status_query == "all":
                self.handle_all_query(current_time)
            else:
                print("Invalid option selected. Exiting.")
        else:
            print("No valid time entered. Exiting.")

    def handle_solo_query(self, current_time):
        """
        Handles the 'solo' query, allowing the user to check the status of one specific package.
        """
        try:
            pkg_id = int(input("Enter the package ID: "))
            pkg = hash_table.lookup(pkg_id)
            if pkg:
                pkg.update_status(current_time)
                hash_table.insert(pkg.get_id(), pkg)
                print(pkg)
            else:
                print(f"Package ID {pkg_id} not found.")
        except ValueError:
            print("Invalid package ID entered. Please enter a valid integer.")

    def handle_all_query(self, current_time):
        """
        Handles the 'all' query, displaying the status of all packages.
        """
        for id in range(1, 41):
            pkg = hash_table.lookup(id)
            if pkg:
                pkg.update_status(current_time)
                print(pkg)
            else:
                print(f"Package ID {id} not found.")

# Instantiate the user interface
ui = UserInterface()
