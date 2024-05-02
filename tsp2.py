import json
import numpy as np
import folium
from folium.plugins import MarkerCluster

REGISTERED_USERS_FILE = "registered_users.json"

registered_users = {}

def load_registered_users():
    global registered_users
    try:
        with open(REGISTERED_USERS_FILE, 'r') as file:
            registered_users = json.load(file)
    except FileNotFoundError:
        registered_users = {}

def save_registered_users():
    with open(REGISTERED_USERS_FILE, 'w') as file:
        json.dump(registered_users, file)

def distance(city1, city2):
    return np.linalg.norm(np.array(city1) - np.array(city2))

def nearest_neighbor_algorithm(cities):
    n = len(cities)
    unvisited_cities = set(range(1, n))
    current_city = 0
    tour = [current_city]

    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: distance(cities[current_city], cities[city]))
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city

    tour.append(tour[0])

    return tour

def register_user(username, password):
    if username in registered_users:
        print("Username already exists. Please choose a different username.")
        return False
    else:
        registered_users[username] = password
        save_registered_users()
        print("Registration successful. You can now log in.")
        print("Registered Users:", registered_users)
        return True

def login(username, password):
    if username in registered_users and registered_users[username] == password:
        print("Login successful.")
        return True
    else:
        print("Invalid username or password.")
        print("Registered Users:", registered_users)
        return False

def plot_optimized_tour(cities_coordinates, optimized_tour_indices):
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(india_map)
    for index in optimized_tour_indices:
        city_coord = cities_coordinates[index]
        folium.Marker(location=city_coord).add_to(marker_cluster)

    for i in range(len(optimized_tour_indices) - 1):
        city1 = cities_coordinates[optimized_tour_indices[i]]
        city2 = cities_coordinates[optimized_tour_indices[i + 1]]
        folium.PolyLine(locations=[city1, city2], color='blue').add_to(india_map)

    # Connect the last city with the first to complete the tour
    city1 = cities_coordinates[optimized_tour_indices[-1]]
    city2 = cities_coordinates[optimized_tour_indices[0]]
    folium.PolyLine(locations=[city1, city2], color='blue').add_to(india_map)

    india_map.save('optimized_tour_map.html')

def plot_tsp_animation(cities_coordinates):
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(india_map)
    for coord in cities_coordinates:
        folium.Marker(location=coord).add_to(marker_cluster)

    # Prompt user to register or login
    while True:
        choice = input("Enter '1' to register, '2' to login: ")
        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            if register_user(username, password):
                break
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login(username, password):
                break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

    # Find the optimized tour using the Nearest Neighbor Algorithm
    optimized_tour_indices = nearest_neighbor_algorithm(cities_coordinates)

    # Connect cities in the optimized tour with lines
    for i in range(len(optimized_tour_indices) - 1):
        city1 = cities_coordinates[optimized_tour_indices[i]]
        city2 = cities_coordinates[optimized_tour_indices[i + 1]]
        folium.PolyLine(locations=[city1, city2], color='blue').add_to(india_map)

    # Connect the last city with the first to complete the tour
    city1 = cities_coordinates[optimized_tour_indices[-1]]
    city2 = cities_coordinates[optimized_tour_indices[0]]
    folium.PolyLine(locations=[city1, city2], color='blue').add_to(india_map)
    india_map.save('optimized_tour_map.html')


load_registered_users()


if __name__ == "__main__":
    # Coordinates of cities in India
    cities_coordinates = [
        (28.6139, 77.2090),  # Delhi
        (19.0760, 72.8777),  # Mumbai
        (12.9716, 77.5946),  # Bangalore
        (22.5726, 88.3639),  # Kolkata
        (26.2389, 73.0243),  # Jodhpur
        (9.2876, 79.3129),   # Rameswaram
        (18.5204, 73.8567),  # Pune
        (25.3176, 82.9739),  # Varanasi
        (17.3850, 78.4867),  # Hyderabad
        (17.6868, 83.2185),  # Visakhapatnam
        (21.1702, 72.8311),  # Surat
        (9.9312, 76.2673),    # Kochi
        (34.1526, 77.5771),  #Leh
        (23.2599, 77.4126)  #Bhopal
    ]

    plot_tsp_animation(cities_coordinates)
