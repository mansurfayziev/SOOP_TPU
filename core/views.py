from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms  import CreateUserForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import RoomNumber, Violation, Akt
from django.http import HttpResponse
from django.contrib import messages

@login_required(login_url='login')
def home(request):

        roomsd = RoomNumber.objects.get(username=request.user).number
        vios = Violation.objects.filter(room=roomsd)[::-1]
        akts= Akt.objects.filter(room=roomsd)[::-1]

        context={
            'room_user':roomsd,
            'vios_len':len(vios),
            'vios': vios,
            'akts': akts,
            'akts_len': len(akts),
        }

        if request.method == 'POST':
            if 'create_act' in request.POST:
                # Если была нажата кнопка "Акт"
                room = request.POST['room']
                fio = request.POST['fio']
                comment = request.POST['comment']
                soop = f'{request.user.last_name} {request.user.first_name}'
                cam_checks = request.POST.getlist('camCheck')
                f = ''
                for check in cam_checks:
                    f += check + '. '
                if comment:
                    f += comment + '. '

                rr = Akt(room=room, fio=fio, comment=f, soop_fio=soop)
                if room and room.isnumeric():
                    rr.save()
                    messages.success(request, 'Успешно: Акт сохранен!')
                else:
                    messages.error(request, 'Ошибка: Номер комнаты не указан!')

                return redirect('home')  # Перенаправьте пользователя на ту же страницу после создания акта

            else:
                room = request.POST['room']
                fio = request.POST['fio']
                comment = request.POST['comment']
                soop = f'{request.user.last_name} {request.user.first_name}'
                cam_checks = request.POST.getlist('camCheck')
                f = ''
                for check in cam_checks:
                    f += check + '. '
                if comment:
                    f += comment + '. '

                rr = Violation(room=room, fio=fio, comment=f, soop_fio=soop)
                if room and room.isnumeric():
                    rr.save()
                    messages.success(request, f'Успешно: Нарушение сохранено! ({room} комната)')
                else:
                    messages.error(request, 'Ошибка: Номер комнаты не указан!')

                return redirect('home')  # Перенаправьте пользователя на ту же страницу после сохранения нарушения




        return render(request, 'core/home.html',context)

        #return HttpResponse("Hello")


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        form=CreateUserForm()

        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                room = form.cleaned_data.get('room')
                rr= RoomNumber(username=user, number=room)

                rr.save()

                messages.success(request, 'Аккаунт создан для '+user)

                return redirect('login')

        return render(request, 'core/signup.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Логин или пароль неверен')


        return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


