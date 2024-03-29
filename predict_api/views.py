from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from utils import get_model, get_weather_data, formate_datetime

from constants import MODLE_ID_RANGE

import json




@csrf_exempt
def predict_by_id(request):
    current_time = datetime.now()
    data = json.loads(request.body)

    # check the passed data is number and in the specific range
    if isinstance(data['id'], int) and (data['id'] in MODLE_ID_RANGE):
        model_id = data['id']
        model = get_model.get_model_by_id(model_id)
    else:
        return JsonResponse({'error': 'Invalid Model Id'}, status=400)

    # get current time from local or frontend
    if bool(data['month']) and (1 <= int(data['month']) <= 12):
        month = data['month']
    else:
        month = current_time.month

    # get current temperature from weather api or frontend
    if bool(data['temp']):
        temp = data['temp']
    else:
        # get temperature from api
        temp = get_weather_data.get_weather_data(current_time)['temp']

    if bool(data['time_of_week']):
        time_of_week = data['time_of_week']
    else:
        time_of_week = formate_datetime.formate_dt_for_model(current_time)

    # check the method of request
    if request.method == 'POST':
        # using prediction model to produce result
        predict_result = model.predict([[temp, month, time_of_week]])[0]

    # return result
    return JsonResponse({
        'Taxi_Zone_ID': model_id,
        'calm_rate': predict_result}
    )


@csrf_exempt
def my_view_function(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Data type recieved:', type(data))
            print('Data Format:', data)
        
            # Process the JSON data as needed
            # For example, you can access specific values using data['key']
            
            # Generate a response JSON
            response_data = {
                'message': 'Data received successfully',
                'received_data': data,
                'statement_from_backend': 'This is a test to get the response'
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    # Return an error if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)