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
import os
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from .obfuscator import obfuscate_code
from django.conf import settings


# Create a logger instance
logger = logging.getLogger("myapp")


# #without static files
# def verify_license(request):
#     if request.method == 'POST':
#         # Get the license key, lname, iblafp, user agent, window size, and script name from the request body
#         data = json.loads(request.body)
#         license_key = data.get('licenseKey')
#         lname = data.get('lname')
#         iblafp = data.get('iblafp')
#         user_agent = data.get('userAgent')
#         window_size = data.get('windowSize')
#         script_name = data.get('scriptName')

#         print(license_key)
#         print(lname)
#         print(iblafp)
#         print(user_agent)
#         print(window_size)
#         print(script_name)

#         # Get the user's IP address
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip_address = x_forwarded_for.split(',')[0]
#         else:
#             ip_address = request.META.get('REMOTE_ADDR')

#         # Check if the license key is valid
#         license_key_obj = LicenseKey.objects.get(key=license_key)

#         if license_key_obj:
#             # Determine the script file path based on the script_name
#             script_file_path = os.path.join('myapp', f'{script_name}.js')

#             # Read the existing JavaScript code
#             try:
#                 with open(script_file_path, 'r') as file:
#                     javascript_code = file.readlines()

#                 # Insert the lname and iblafp values at the top of the file
#                 javascript_code.insert(0, f'let lname = "{lname.strip()}";\n')
#                 javascript_code.insert(1, f'let iblafp = {int(str(iblafp).strip())};\n')

#                 # Log the license key and IP address
#                 logger.info(f"License key '{license_key}' used by IP address {ip_address} user_agent {user_agent} window_size {window_size}")

#                 # Join the lines back into a single string
#                 javascript_code = ''.join(javascript_code)

#                 return JsonResponse({'valid': True, 'code': javascript_code})
#             except FileNotFoundError:
#                 return JsonResponse({'valid': False, 'error': f'Script file not found: {script_file_path}'})
#         else:
#             return JsonResponse({'valid': False})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def verify_license(request):
    if request.method == "POST":
        # Get the license key, lname, iblafp, user agent, window size, and script name from the request body
        data = json.loads(request.body)
        license_key = data.get("licenseKey")
        lname = data.get("lname")
        iblafp = data.get("iblafp")
        user_agent = data.get("userAgent")
        window_size = data.get("windowSize")
        script_name = data.get("scriptName")

        # print(license_key)
        # print(lname)
        # print(iblafp)
        # print(user_agent)
        # print(window_size)
        # print(script_name)

        # Get the user's IP address
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        # Check if the license key is valid
        license_key_obj = LicenseKey.objects.get(key=license_key)

        if license_key_obj:
            # Determine the script file path based on the script_name
            script_file_name = f"{script_name}.js"
            script_file_path = finders.find("myapp/js/" + script_file_name)

            # Read the existing JavaScript code
            try:
                with open(script_file_path, "r") as file:
                    javascript_code = file.readlines()

                # Insert the lname and iblafp values at the top of the file
                javascript_code.insert(0, f'let lname = "{lname.strip()}";\n')
                javascript_code.insert(1, f"let iblafp = {int(str(iblafp).strip())};\n")

                # Log the license key and IP address
                logger.info(
                    f"License key '{license_key}' used by IP address {ip_address} user_agent {user_agent} window_size {window_size}"
                )

                # Join the lines back into a single string
                javascript_code = "".join(javascript_code)

                # javascript_code =   obfuscate_code(javascript_code)

                return JsonResponse({"valid": True, "code": javascript_code})
            except ValueError:
                return JsonResponse(
                    {
                        "valid": False,
                        "error": f"Script file not found: {script_file_path}",
                    }
                )
            except TypeError:
                return JsonResponse(
                    {
                        "valid": False,
                        "error": f"Script file not found: {script_file_path}",
                    }
                )
            except FileNotFoundError:
                return JsonResponse(
                    {
                        "valid": False,
                        "error": f"Script file not found: {script_file_path}",
                    }
                )
        else:
            return JsonResponse({"valid": False})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


# views.py


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


def get_user_ip(request):
    client_ip, _ = get_client_ip(request)
    if client_ip is None:
        return JsonResponse({"error": "Unable to retrieve IP address"}, status=400)
    else:
        return JsonResponse({"ip_address": client_ip})


@login_required
def license_manager(request):
    return render(request, "license_manager.html")


def license_key_list(request):
    license_keys = list(
        LicenseKey.objects.values("id", "key", "created_at", "updated_at")
    )
    return JsonResponse(license_keys, safe=False)


def license_key_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        license_key = LicenseKey(key=data["key"])
        license_key.save()
        return JsonResponse(
            {
                "id": license_key.id,
                "key": license_key.key,
                "created_at": license_key.created_at,
                "updated_at": license_key.updated_at,
            }
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)


def license_key_update(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse({"error": "License key not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        license_key.key = data["key"]
        license_key.save()
        return JsonResponse(
            {
                "id": license_key.id,
                "key": license_key.key,
                "created_at": license_key.created_at,
                "updated_at": license_key.updated_at,
            }
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)


def license_key_delete(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse({"error": "License key not found"}, status=404)

    if request.method == "DELETE":
        license_key.delete()
        return JsonResponse({"message": "License key deleted"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def delete_license_key(request, pk):
    try:
        license_key = LicenseKey.objects.get(pk=pk)
    except LicenseKey.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "License key not found"}, status=404
        )

    if request.method == "DELETE":
        license_key.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )


def get_license_keys(request):
    search_term = request.GET.get("search", "").lower()
    license_keys = (
        LicenseKey.objects.filter(
            Q(name__icontains=search_term) | Q(key__icontains=search_term)
        )
        .values("id", "name", "key", "created_at")
        .order_by("-created_at")
    )

    page_number = request.GET.get("page", 1)
    paginator = Paginator(license_keys, 10)  # Show 10 license keys per page

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    license_keys_data = list(page_obj.object_list)
    for key in license_keys_data:
        key["created_at"] = key["created_at"].strftime("%Y-%m-%d %H:%M:%S")

    response_data = {
        "license_keys": license_keys_data,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
    }

    return JsonResponse(response_data, safe=False)


def create_license_key(request):
    if request.method == "POST":
        data = json.loads(request.body)
        license_key_name = data.get("name")
        license_key_value = data.get("key")

        if license_key_name and license_key_value:
            try:
                license_key_obj = LicenseKey.objects.create(
                    name=license_key_name, key=license_key_value
                )
                license_keys = list(
                    LicenseKey.objects.values("id", "name", "key", "created_at")
                )
                for key in license_keys:
                    key["created_at"] = key["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                return JsonResponse({"success": True, "license_keys": license_keys})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        else:
            return JsonResponse(
                {"success": False, "error": "License key name and key are required"}
            )
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )


def show_logs(request):
    # log_file_path = "logs/license_keys.log"
    # Construct the log file path using BASE_DIR and os.path.join
    log_file_path = os.path.join(settings.BASE_DIR, "logs", "license_keys.log")
    try:
        with open(log_file_path, "r") as log_file:
            log_contents = log_file.readlines()
            log_contents.reverse()  # Reverse the order of lines

            # Pagination
            page = int(request.GET.get("page", 1))
            logs_per_page = 20
            total_logs = len(log_contents)
            total_pages = math.ceil(total_logs / logs_per_page)

            start_index = (page - 1) * logs_per_page
            end_index = start_index + logs_per_page
            paginated_logs = log_contents[start_index:end_index]

            # Remove the "views" part and the number "7216" from each log entry
            paginated_logs = [
                re.sub(r"views \d+\s+\d+\s+", "", line) for line in paginated_logs
            ]

            response_data = {
                "logs": paginated_logs,
                "total_pages": total_pages,
            }

            return JsonResponse(response_data)
    except FileNotFoundError:
        return JsonResponse({"error": "Log file not found."}, status=404)


@login_required
def show_logs_html(request):
    return render(request, "show_logs.html")


def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": False, "error": "Invalid username or password"}
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login_url")




def show_static_files(request):
    static_files = []
    for finder in finders.get_finders():
        for path, storage in finder.list(["admin"]):
            if path.endswith(".js"):
                static_files.append({"path": path, "name": os.path.basename(path)})

    if request.method == "POST":
        file_to_delete = request.POST.get("file_to_delete")
        if file_to_delete:
            for finder in finders.get_finders():
                for path, storage in finder.list(["adming"]):
                    if path.endswith(file_to_delete):
                        file_path = storage.path(path)
                        try:
                            os.remove(file_path)
                            static_files = [
                                f for f in static_files if f["name"] != file_to_delete
                            ]
                            break
                        except Exception as e:
                            print(f"Error deleting file: {e}")

    context = {
        "static_files": static_files,
    }
    return render(request, "static_files.html", context)




def show_static_files(request):
    static_files = []
    for finder in finders.get_finders():
        for path, storage in finder.list(["admin"]):
            if path.endswith(".js"):
                static_files.append({"path": path, "name": os.path.basename(path)})

    return JsonResponse(static_files, safe=False)





def delete_file(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_path = data.get("file_path")
            print(file_path)  # This should now print the correct file_path value
            if file_path:
                for finder in finders.get_finders():
                    for path, storage in finder.list(["admin"]):
                        if path == file_path:
                            file_full_path = storage.path(path)
                            try:
                                os.remove(file_full_path)
                                return JsonResponse({"success": True})
                            except Exception as e:
                                return JsonResponse({"success": False, "error": str(e)})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


def files(request):
    return render(request, "files.html")




def upload_static_file(request):
    if request.method == "POST":
        try:
            static_file = request.FILES["static_file"]
            file_name = static_file.name

            # Construct the file path using BASE_DIR and os.path.join
            static_dir = os.path.join(
                settings.BASE_DIR, "myapp", "static", "myapp", "js"
            )
            print(static_dir)
            file_path = os.path.join(static_dir, file_name)

            # Create the directory if it doesn't exist
            os.makedirs(static_dir, exist_ok=True)

            # Save the uploaded file to the static directory
            with open(file_path, "wb+") as destination:
                for chunk in static_file.chunks():
                    destination.write(chunk)

            return JsonResponse(
                {"success": True, "message": "File uploaded successfully"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
