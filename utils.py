import datetime

#To fix times like 1:3, to make it look like 01:03, or dates like 4/8/2018, to make it look like 04/08/2018
def filling(number):
    if (number < 10):
        if (number == 0):
            return "00"
        else:
            return("0"+str(number))
    else:
        return(str(number))

#To get current date and time
def now1():
    return datetime.datetime.now()

#To create and compare a super KEY to check that a new address exists or not in a database  
def checking_existing_address_in_db(street, city, state, zipcode, places_in_database):        
    key_place_html_form = street+city+state+zipcode
    #print(key_place_html_form)
    #Validating if there is a place in the database with the same name
    if (places_in_database.count() == 0):
        existing_place = False
    else:
        for place_in_list in places_in_database:
            key_place_database = place_in_list.streetaddress+place_in_list.city+place_in_list.state+place_in_list.zipcode 
            #print(key_place_database)        
            if key_place_database == key_place_html_form:
                existing_place = True
            else:
                existing_place = False
    return existing_place

#To create and compare a super KEY to check if a new event exists or not in a database  
def checking_existing_event_in_db(name, hobby, place, date, time, events_in_database):   
    key_event_form = name+hobby.name+place.unique_key_address+date+time  
    print(key_event_form)
    #Validating if there is an event in the database with the same name
    if (events_in_database.count() == 0):
        existing_event = False
    else:
        existing_event = False
        for event in events_in_database:
            key_event_database = event.event_key 
            print(key_event_database)        
            if key_event_database == key_event_form:
                existing_event = True            
    return existing_event

#To help organizing events in future, present and past. date_time_order (dto)
def dto(date_time_present):   
    return filling(date_time_present.year)+filling(date_time_present.month)+filling(date_time_present.day)+filling(date_time_present.hour)+filling(date_time_present.minute)

#To help organizing events in future, present and past. date_time_order (dto)
def dte(duration_event):  
    return int(str(duration_event[0:2])+str(duration_event[3:5])) 
    
