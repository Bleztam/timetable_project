from django.http import JsonResponse
import os
import json
from django.core.files.storage import FileSystemStorage

DATA_DIR = os.path.join('timetable','data')

def get_latest_json_file():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    if not files:
        return None, None 
    files.sort(key=lambda f:int(f.split('_v')[1].split('.json')[0]), reverse=True)
    latest_file = files[0]
    version = int(latest_file.split('_v')[1].split('.json')[0])
    return latest_file, version

def fetch_latest_timetable(request):
    latest_file, version = get_latest_json_file()
    if not latest_file:
        return JsonResponse({'error': 'No timetable available'}, status=404)
    with open(os.path.join(DATA_DIR, latest_file), 'r') as file:
        data = json.load(file)
        return JsonResponse({'version' : version, 'timetable' : data})
    
def check_timetable_version(request):
    client_version = int(request.GET.get('version', 0))
    _, latest_version = get_latest_json_file()

    if latest_version is None:
        return JsonResponse({'error': 'No timetable available'}, status=404)

    if client_version < latest_version:
        return JsonResponse({'update_required': True, 'latest_version': latest_version})
    else:
        return JsonResponse({'update_required': False, 'latest_version': latest_version})
    



def upload_timetable(request):
    if request.method == 'POST' and request.FILES.get('file'):
        version = request.POST.get('version')

        if not version or not version.isdigit():
            return JsonResponse({'error': 'Invalid version'}, status=400)

        file_name = f'timetable_v{version}.json'
        if os.path.exists(os.path.join(DATA_DIR, file_name)):
            return JsonResponse({'error': 'Version already exists'}, status=400)

        fs = FileSystemStorage(location=DATA_DIR)
        fs.save(file_name, request.FILES['file'])
        return JsonResponse({'message': 'File uploaded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# from django.http import JsonResponse

# def fetch_latest_timetable(request):
#     return JsonResponse({"message": "This is the latest timetable!"})

# def check_timetable_version(request):
#     return JsonResponse({"message": "Version check endpoint!"})

# def upload_timetable(request):
#     return JsonResponse({"message": "Upload endpoint!"})