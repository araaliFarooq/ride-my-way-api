""" functionality to run the created models"""
from app import app
import random, json
from flask import Flask, request, json, jsonify
from app.models import User, Driver, RideOffer, RideRequest


Users = [
{"id": "1",
"firstname":"shakira", 
"secondname": "kyra",
"username":"kyooq",
"contact": "0888887676",
"user_category":"driver",
"password":"farooq",
"car_type":"rover",
"reg_num":"uab1234",
"lic_num":"4567789999"
},
{"id": "2",
"firstname":"Araali", 
"secondname": "farooq",
"username":"kyooq",
"contact": "0888642226",
"user_category":"passenger",
"password":"farooq"
}
]

all_offers = [{
"id":"1",
"driver_name":"shakira", 
"location": "kawempe",
"car_type":"rover",
"plate_number": "uab 123x",
"contact":"0706058595",
"availability":"10am - 10pm",
"cost_per_km":"200"
}]

all_requests = []

"""registering new user"""
@app.route("/api/v1/register", methods=["POST"])
def register():
    
    data = request.get_json()
    firstname = data.get("firstname")
    secondname = data.get("secondname")
    username = data.get("username")
    contact = data.get("contact")
    user_category = data.get("user_category")
    password = data.get("password")

    id = len(Users) + 1

    if len(firstname) < 1:
        return jsonify({"mais missing"}), 400
    if len(secondname) < 1:
        return jsonify({"ma is missing"}), 400
    if len(username) < 1:
        return jsonify({"message":"username is missing"}), 400
    if len(contact) < 1:
        return jsonify({"message":"contact is missing"}), 400
    if len(user_category) < 1:
        return jsonify({"message":"User category is missing"}), 400
    if len(password) < 1:
        return jsonify({"message":"password is missing"}), 400

    """checking is user is a driver or passenger"""
    if user_category == "driver":
        car_type = data.get("car_type")
        reg_num = data.get("reg_num")
        lic_num = data.get("lic_num")
        new_user = Driver(id, firstname, secondname, username, contact, user_category, car_type, reg_num, lic_num, password)
        Users.append(new_user)
        return jsonify({"message":"New Driver successfully registered"}), 201

    new_user = User(id,firstname,secondname,username,contact, user_category, password )
    Users.append(new_user)
    return jsonify({"message":"New Client successfully registered"}), 201

""" logging in a registered user"""
@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    

    if len(username) < 1:
        return jsonify({"message": "Missing or Wrong username"}), 400
    if len(password) < 1:
        return jsonify({"message": "Missing or Wrong password"}), 400

    return jsonify({"message": "Successfully Logged in"}), 200


""" adding a ride offer"""
@app.route("/api/v1/rides/add_offer", methods=["POST"])
def add_offer():   
    data = request.get_json()
    driver_name = data.get("driver_name")
    location = data.get("location")
    car_type = data.get("car_type")
    plate_number = data.get("plate_number")
    contact = data.get("contact")
    availability = data.get("availability")
    cost_per_km = data.get("cost_per_km")


    if len(driver_name) < 1:
        return jsonify({"message":"Drivers name is missing"}), 400
    if len(location) < 1:
        return jsonify({"message":"Location is missing"}), 400
    if len(car_type) < 1:
        return jsonify({"message":"Car type is missing"}), 400
    if len(plate_number) < 1:
        return jsonify({"message":"Plate number is missing"}), 400
    if len(contact) < 1:
        return jsonify({"message":"Contact is missing"}), 400
    if len(availability) < 1:
        return jsonify({"message":"Working hours not stated"}), 400
    if len(cost_per_km) < 1:
        return jsonify({"message":"Charge per Km not stated"}), 400

    id = len(all_offers) + 1

    new_offer = RideOffer(id, driver_name, location, car_type, plate_number, contact, availability, cost_per_km)
    all_offers.append(new_offer)
    return jsonify({"message":"Your offer has been registered"}), 201

        
"""Getting all available ride offers"""
@app.route("/api/v1/rides/all_offers", methods=["GET"])
def get_all_offers():

    my_offers = []

    if len(all_offers) > 0:
        for offer in all_offers:
            offer_data = {
            "id": offer["id"],
            "Driver": offer["driver_name"],
            "Location": offer["location"],
            "Car Type": offer["car_type"],
            "Plate Number": offer["plate_number"],
            "Phone Number": offer["contact"],
            "Availability": offer["availability"],
            "Cost/Km": offer["cost_per_km"]
        }

            my_offers.append(offer_data)
        return jsonify({"Available Offers": my_offers}), 200

    return jsonify({"message":"No offer has been registered yet"}), 404  


"""Fetching a single ride offer"""
@app.route("/api/v1/rides/<ride_id>", methods=["GET"])
def get_single_ride(ride_id):
    
    if len(all_offers) > 0:
        for offer in all_offers:
            if int(offer["id"]) == int(ride_id):
                offer_data = {
                    "id": offer["id"],
                    "Driver": offer["driver_name"],
                    "Location": offer["location"],
                    "Car Type": offer["car_type"],
                    "Plate Number": offer["plate_number"],
                    "Phone Number": offer["contact"],
                    "Availability": offer["availability"],
                    "Cost/Km": offer["cost_per_km"]
                }
                
                return jsonify({"Offer": offer_data}), 200

            return jsonify({"mesrequester_destination = self.destinationsage":"No match found"}), 404

    return jsonify({"message":"No offer has been registered yet"}), 404  
        

"""making a request to join ride offer"""
@app.route("/api/v1/<user_id>/<offer_id>/requests", methods=["POST","GET"])
def send_ride_request(user_id,offer_id):
    
    requests_data = []

    if len(all_offers) > 0:
        for offer in all_offers:
            if int(offer["id"]) == int(offer_id):
                request_id = offer["id"]
                location = offer["location"]

    for user in Users:
       if int(user["id"]) == int(user_id):
           request_data ={
               "Ride ID": request_id,
               "Requester ID": user["id"],
               "Clients Name": user["firstname"] +" "+ user["secondname"],
               "Phone Number": user["contact"],
               "Location": location
           }
    id = len(all_requests) + 1       
    client_name = user["firstname"] +" "+ user["secondname"]
    phone_num = user["contact"]
    address = location

    new_request = RideRequest(id, client_name, phone_num, address)
    all_requests.append(new_request)


    return jsonify({"message": "Request sent successfully", "Request": request_data }), 201     