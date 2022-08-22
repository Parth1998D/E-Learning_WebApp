import random
import string
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, hashers, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import OrderForm, InterestForm, StudentForm, PasswordResetForm
from .models import Topic, Course, Student


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more than one hour ago'
    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login})


def about(request):
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'about_visits': request.session['about_visits']})


def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    course_list = Course.objects.filter(topic=top_no)
    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list})


def courses(request):
    courlist = Course.objects.all()
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            students = Student.objects.filter(pk=request.user.id)
            if len(students) == 1:
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    if order.levels <= order.course.stages:
                        order.student = students[0]
                        order.save()
                        if order.course.price > 150:
                            order.course.discount()
                        msg = 'Your course has been ordered successfully.'
                    else:
                        msg = 'You exceeded the number of levels for this course.'
            else:
                msg = 'You are not a registered student!'
        else:
            msg = "Please Login to place your order!"
        return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    course = get_object_or_404(Course, pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["interested"] == "1":
                course.interested = course.interested + 1
                course.save()
            return redirect('/myapp/')
    else:
        form = InterestForm()
        return render(request, 'myapp/coursedetail.html', {'form': form, 'course': course})


def user_login(request):
    if request.method == 'POST':
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        #     print("test cookie worked")
        # else:
        #     print("test cookie didn't work")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime("%H:%M:%S - %B %d, %Y")
                request.session.set_expiry(3600)
                # request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('myapp:my_account'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        # request.session.set_test_cookie()
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    # request.session.flush()
    # for key in list(request.session.keys()):
    #     del request.session[key]
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required()
def my_account(request):
    students = Student.objects.filter(pk=request.user.id)
    if len(students) == 1:
        student = students[0]
        return render(request, 'myapp/my_account.html', {'fullName': student.first_name + " " + student.last_name,
                                                         'image': student.image,
                                                         'orders': student.orders.all(),
                                                         'interested_in': student.interested_in.all()
                                                         })
    else:
        return HttpResponse('You are not a registered student!')


def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(student.password)
            student.save()
            form.save_m2m()

            msg = 'Congratulations, You are now registered as a student'
            return render(request, 'myapp/register_response.html', {'msg': msg})
    else:
        form = StudentForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def myorders(request):
    students = Student.objects.filter(pk=request.user.id)
    if len(students) == 1:
        orders = students[0].orders.all()
        return render(request, 'myapp/myorders.html', {'student': students[0], 'orders': orders})
    else:
        return render(request, 'myapp/myorders.html')


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            curr_student = Student.objects.get(username=username)
            email = curr_student.email
            passwordString = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            passwordEncrypted = hashers.make_password(passwordString)
            curr_student.password = passwordEncrypted
            curr_student.save()
            message = "Your password has been changed successfully. Please find your new password: " + passwordString
            send_mail('Password changed successfully',
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
            return render(request, 'myapp/reset_password.html', {'email': email})
    else:
        form = PasswordResetForm()
    return render(request, 'myapp/reset_password.html')
