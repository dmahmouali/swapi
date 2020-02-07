import requests, json, time

from requests_futures.sessions import FuturesSession
from concurrent.futures import ProcessPoolExecutor 
from flask import Flask, render_template,url_for, request

app = Flask(__name__)

#Decorator to calculate time of method execution 
def calculate_time(method):
    try:
        def timed(*args, **kw):
            start_time= time.time()
            execute_method = method(*args, **kw)
            end_time= time.time()
            print ('%r  %.2f s' % (method.__name__,(end_time-start_time)))
            return execute_method
        return timed    
    except expression:
        pass

def get_parlell_respons(arr_urls, attribute_name):
    try:
        #create return container
        return_pool = []
        #start session
        with FuturesSession() as session:
            futures = [session.get(url) for url in arr_urls]
            for future in futures:
                #check attribute decleration 
                if attribute_name != 'indefinite':
                    return_data = json.loads(future.result().text)[attribute_name]
                    return_pool.append(return_data)
                else:
                    return_pool = ['can not find']
        return return_pool    
    except expression:
        pass


@calculate_time
def build_context():
    try:
        return_context = {}

        #get text from user UI
        textsearch = request.form['textsearch']
        
        #handle input
        textsearch = textsearch.strip()
        if not textsearch:
            return "Please Enter much information"
        
        #access server for get response
        url = 'https://swapi.co/api/people?search='+textsearch
        return_data_json = requests.get(url = url)
        print(url)
        
        #check result
        return_data = json.loads(return_data_json.text)
        if int(return_data["count"]) != 1:
            return "Please Enter much information"
        
        #person name
        person_name = return_data["results"][0]['name']
        print("Nmae is : ", person_name)
        return_context['person_name'] = person_name

        #person gender
        person_gender = return_data["results"][0]['gender']
        print("Gender is : ", person_gender)
        return_context['person_gender'] = person_gender
        
        #get species name list
        species = get_parlell_respons(return_data["results"][0]["species"], 'name')
        print("species   :   " , species)
        return_context['species'] = species[:]

        #get average lifespan list
        average_lifespan = get_parlell_respons(return_data["results"][0]["species"], 'average_lifespan')
        print("average_lifespan   :   " , average_lifespan)
        return_context['average_lifespan'] = average_lifespan[:]

        #get home planet name from server
        home_planet_name = get_parlell_respons([return_data["results"][0]["homeworld"]], 'name')
        print("the home planet is : ",home_planet_name)
        return_context['home_planet_name'] = home_planet_name[:]
        #get film's name list
        films = get_parlell_respons(return_data["results"][0]["films"], 'title')
        print("films  :  ",films)
        return_context['films'] = films[:]

        return return_context
    except expression:
        pass

@app.route('/', methods=['POST','GET'])
def index():
    #input('Enter Text: ')
    if request.method == 'POST':
        context = build_context()
        #render context to UI frontend
        return render_template('index.html',context = context)
        
    else:
        #in get request render page
        return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)