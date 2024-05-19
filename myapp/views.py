from django.shortcuts import render

# Create your views here.
# license_verification/views.py
from django.http import JsonResponse
import json
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from ipware import get_client_ip
from .models import LicenseKey
from .forms import LicenseKeyForm
from django.core.paginator import Paginator
from django.db.models import Q
import re
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import math

# Create a logger instance
logger = logging.getLogger('myapp')

# List of valid license keys
valid_license_keys = ["ABC123", "DEF456", "GHI789"]

with open('myapp/demo.js', 'r') as file:
    javascript_code = file.read()









# @csrf_exempt
# def verify_license(request):
#     if request.method == 'POST':
#         # Get the license key from the request body
#         data = json.loads(request.body)
#         license_key = data.get('licenseKey')

#         # Check if the license key is valid
#         if license_key in valid_license_keys:
#             return JsonResponse({'valid': True, 'code': javascript_code})
#         else:
#             return JsonResponse({'valid': False})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

# @csrf_exempt
# def verify_license(request):
#     if request.method == 'POST':
#         # Get the license key from the request body
#         data = json.loads(request.body)
#         license_key = data.get('licenseKey')

#         # Get the user's IP address
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         print(x_forwarded_for)
#         if x_forwarded_for:
#             ip_address = x_forwarded_for.split(',')[0]
#         else:
#             ip_address = request.META.get('REMOTE_ADDR')

#         # Check if the license key is valid
#         if license_key in valid_license_keys:
#             # Log the license key and IP address
#             logger.info(f"License key '{license_key}' used by IP address {ip_address}")

#             return JsonResponse({'valid': True, 'code': javascript_code})
#         else:
#             return JsonResponse({'valid': False})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def verify_license(request):
    if request.method == 'POST':
        # Get the license key from the request body
        data = json.loads(request.body)
        license_key = data.get('licenseKey')

        # Get the user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        try:
            # Check if the license key exists in the database
            license_key_obj = LicenseKey.objects.get(key=license_key)

            # Log the license key and IP address
            logger.info(f"License key '{license_key}' used by IP address {ip_address}")

            # Return the JavaScript code if the license key is valid
            return JsonResponse({'valid': True, 'code': javascript_code})
        except LicenseKey.DoesNotExist:
            # Return False if the license key is not found in the database
            return JsonResponse({'valid': False})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# views.py


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def get_user_ip(request):
    client_ip, _ = get_client_ip(request)
    if client_ip is None:
        return JsonResponse({'error': 'Unable to retrieve IP address'}, status=400)
    else:
        return JsonResponse({'ip_address': client_ip})


# def license_key_list(request):
#     license_keys = LicenseKey.objects.all()
#     return render(request, 'license_manager/license_key_list.html', {'license_keys': license_keys})


# def license_key_create(request):
#     if request.method == 'POST':
#         form = LicenseKeyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('license_key_list')
#     else:
#         form = LicenseKeyForm()
#     return render(request, 'license_manager/license_key_form.html', {'form': form})

# def license_key_update(request, pk):
#     license_key = get_object_or_404(LicenseKey, pk=pk)
#     if request.method == 'POST':
#         form = LicenseKeyForm(request.POST, instance=license_key)
#         if form.is_valid():
#             form.save()
#             return redirect('license_key_list')
#     else:
#         form = LicenseKeyForm(instance=license_key)
#     return render(request, 'license_manager/license_key_form.html', {'form': form})



# def license_key_delete(request, pk):
#     license_key = get_object_or_404(LicenseKey, pk=pk)
#     if request.method == 'POST':
#         license_key.delete()
#         return redirect('license_key_list')
#     return render(request, 'license_manager/license_key_confirm_delete.html', {'license_key': license_key})

@login_required
def license_manager(request):
    return render(request, 'license_manager.html')




def license_key_list(request):
    license_keys = list(LicenseKey.objects.values('id', 'key', 'created_at', 'updated_at'))
    return JsonResponse(license_keys, safe=False)

def license_key_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        license_key = LicenseKey(key=data['key'])
        license_key.save()
        return JsonResponse({'id': license_key.id, 'key': license_key.key, 'created_at': license_key.created_at, 'updated_at': license_key.updated_at})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def license_key_update(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse({'error': 'License key not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        license_key.key = data['key']
        license_key.save()
        return JsonResponse({'id': license_key.id, 'key': license_key.key, 'created_at': license_key.created_at, 'updated_at': license_key.updated_at})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def license_key_delete(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse({'error': 'License key not found'}, status=404)

    if request.method == 'DELETE':
        license_key.delete()
        return JsonResponse({'message': 'License key deleted'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# def create_license_key(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         license_name = data.get('name')
#         license_key = data.get('key')
#         if license_key:
#             try:
#                 license_key_obj = LicenseKey.objects.create(name=license_name, key=license_key)
#                 return JsonResponse({'success': True, 'key': license_key_obj.key})
#             except Exception as e:
#                 return JsonResponse({'success': False, 'error': str(e)})
#         else:
#             return JsonResponse({'success': False, 'error': 'License key is required'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


    


# def get_license_keys(request):
#     license_keys = list(LicenseKey.objects.values_list('key', flat=True))
#     return JsonResponse(license_keys, safe=False)


# def get_license_keys(request):
#     license_keys = list(LicenseKey.objects.values('key', 'created_at'))
#     for key in license_keys:
#         key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')
#     return JsonResponse(license_keys, safe=False)


# def get_license_keys(request):
#     license_keys = list(LicenseKey.objects.values('name', 'key', 'created_at'))
#     for key in license_keys:
#         key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')
#     return JsonResponse(license_keys, safe=False)

# def get_license_keys(request):
#     license_keys = list(LicenseKey.objects.values('id', 'name', 'key', 'created_at'))
#     for key in license_keys:
#         key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')
#     return JsonResponse(license_keys, safe=False)




def delete_license_key(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'License key not found'}, status=404)

    if request.method == 'DELETE':
        license_key.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)







# def get_license_keys(request):
#     page_number = request.GET.get('page', 1)
#     license_keys = LicenseKey.objects.values('id', 'name', 'key', 'created_at')
#     paginator = Paginator(license_keys, 10)  # Show 10 license keys per page

#     try:
#         page_obj = paginator.page(page_number)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)

#     license_keys_data = list(page_obj.object_list)
#     for key in license_keys_data:
#         key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')

#     response_data = {
#         'license_keys': license_keys_data,
#         'current_page': page_obj.number,
#         'total_pages': paginator.num_pages,
#     }

#     return JsonResponse(response_data, safe=False)


def get_license_keys(request):
    search_term = request.GET.get('search', '').lower()
    license_keys = LicenseKey.objects.filter(
        Q(name__icontains=search_term) | Q(key__icontains=search_term)
    ).values('id', 'name', 'key', 'created_at').order_by('-created_at')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(license_keys, 10)  # Show 10 license keys per page

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    license_keys_data = list(page_obj.object_list)
    for key in license_keys_data:
        key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')

    response_data = {
        'license_keys': license_keys_data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
    }

    return JsonResponse(response_data, safe=False)




def create_license_key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        license_key_name = data.get('name')
        license_key_value = data.get('key')

        if license_key_name and license_key_value:
            try:
                license_key_obj = LicenseKey.objects.create(name=license_key_name, key=license_key_value)
                license_keys = list(LicenseKey.objects.values('id', 'name', 'key', 'created_at'))
                for key in license_keys:
                    key['created_at'] = key['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                return JsonResponse({'success': True, 'license_keys': license_keys})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'License key name and key are required'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)






# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.read()
#         return HttpResponse(log_contents, content_type='text/plain')
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)



# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.readlines()
#             log_contents = ''.join([line + '<br>' for line in log_contents])
#         return HttpResponse(log_contents)
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)

# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.readlines()
#             log_contents = ''.join([line + '<br>' for line in log_contents])
#         return HttpResponse(log_contents, content_type='text/html')
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)


# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.readlines()
#             log_contents.reverse()  # Reverse the order of lines
#             log_contents = ''.join([line + '<br>' for line in log_contents])
#         return HttpResponse(log_contents, content_type='text/html')
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)


# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.readlines()
#             log_contents.reverse()  # Reverse the order of lines
            
#             # Remove the "views" part from each log entry
#             log_contents = [re.sub(r'views \d+\s+', '', line) + '<br>' for line in log_contents]
            
#             log_contents = ''.join(log_contents)
#         return HttpResponse(log_contents, content_type='text/html')
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)


# def show_logs(request):
#     log_file_path = "logs/license_keys.log"
#     try:
#         with open(log_file_path, 'r') as log_file:
#             log_contents = log_file.readlines()
#             log_contents.reverse()  # Reverse the order of lines
            
#             # Remove the "views" part and the number "7216" from each log entry
#             log_contents = [re.sub(r'views \d+\s+\d+\s+', '', line) + '<br>' for line in log_contents]
            
#             log_contents = ''.join(log_contents)
#         return HttpResponse(log_contents, content_type='text/html')
#     except FileNotFoundError:
#         return HttpResponse('Log file not found.', status=404)

def show_logs(request):
    log_file_path = "logs/license_keys.log"
    try:
        with open(log_file_path, 'r') as log_file:
            log_contents = log_file.readlines()
            log_contents.reverse()  # Reverse the order of lines

            # Pagination
            page = int(request.GET.get('page', 1))
            logs_per_page = 20
            total_logs = len(log_contents)
            total_pages = math.ceil(total_logs / logs_per_page)

            start_index = (page - 1) * logs_per_page
            end_index = start_index + logs_per_page
            paginated_logs = log_contents[start_index:end_index]

            # Remove the "views" part and the number "7216" from each log entry
            paginated_logs = [re.sub(r'views \d+\s+\d+\s+', '', line) for line in paginated_logs]

            response_data = {
                'logs': paginated_logs,
                'total_pages': total_pages,
            }

            return JsonResponse(response_data)
    except FileNotFoundError:
        return JsonResponse({'error': 'Log file not found.'}, status=404)





@login_required
def show_logs_html(request):
    return render(request, 'show_logs.html')



# def user_login(request):
#     return render(request, 'login.html')


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')





def logout_view(request):
    logout(request)
    return redirect('login_url') 