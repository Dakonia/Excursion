from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseForbidden
from django.db.models import Count, Avg, Q
from django.contrib import messages


# Стартовая страница
def home(request):
    if request.user.is_authenticated:
        if request.user.is_client():
            return redirect('client')  
        elif request.user.is_company():
            return redirect('company') 
        
    login_form = CustomAuthenticationForm(data=request.POST or None)
    error_message = ""

    if request.method == 'POST':
        if login_form.is_valid(): 
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                if user.role == 'client':
                    return JsonResponse({'success': True, 'redirect_url': 'client'})  
                elif user.role == 'company':
                    return JsonResponse({'success': True, 'redirect_url': 'company'})
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                error_message = "Введите верную почту или пароль."
        else:
            error_message = "Введите верную почту или пароль."
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': error_message})

    return render(request, 'home.html', {'login_form': login_form, 'error_message': error_message})


# Страница клиента
def client_page(request):
    user = request.user
    if not user.is_client():
        return redirect('company')
    
    login_form = AuthenticationForm(data=request.POST or None)
    context = {'login_form': login_form}

    if request.user.is_authenticated and request.user.is_client():
        profile = request.user.client_profile
        context.update({
            'name': profile.name,
            'avatar': profile.image.url if profile.image else None
        })
    buses = Bus.objects.all()
    buses = buses.annotate(
        avg_rating=Avg('transport_company__reviews__stars'),
        reviews_count=Count('transport_company__reviews')
    )

    seats = request.GET.getlist('seats')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    bus_types = request.GET.getlist('bus-type')
    rating = request.GET.getlist('rating')
    long_term = request.GET.getlist('long-term')

    if seats:
        seat_ranges = {
            'до 10': (0, 10),
            '10-20': (10, 20),
            '20-30': (20, 30),
            '30-45': (30, 45),
            '45-60': (45, 60),
            '60+': (60, 1000),
        }
        seat_filters = Q()
        for seat_range in seats:
            if seat_range in seat_ranges:
                min_seats, max_seats = seat_ranges[seat_range]
                seat_filters |= Q(seats__gte=min_seats, seats__lt=max_seats)
        buses = buses.filter(seat_filters)

    if price_min and price_max:
        buses = buses.filter(price_per_day__gte=price_min, price_per_day__lte=price_max)

    if bus_types:
        buses = buses.filter(type__in=bus_types)

    if rating:
        rating_filters = Q()
        for rate in rating:
            if rate == '5':
                rating_filters |= Q(transport_company__reviews__stars=5)
            elif rate == '4+':
                rating_filters |= Q(transport_company__reviews__stars__gte=4)
            elif rate == '3+':
                rating_filters |= Q(transport_company__reviews__stars__gte=3)
            elif rate == '2-':
                rating_filters |= Q(transport_company__reviews__stars__lt=2)

        buses = buses.filter(rating_filters)

    if long_term:
        if 'да' in long_term:
            buses = buses.filter(long_trips=True)
        if 'нет' in long_term:
            buses = buses.filter(long_trips=False)

    context['buses'] = buses
    return render(request, 'client.html', context)




# Профиль
@login_required
def profile(request):           
    user = request.user
    if not user.is_client():
        return redirect('company')
    login_form = AuthenticationForm(data=request.POST or None)
    context = {'login_form': login_form}
    
    if request.user.is_authenticated and request.user.is_client():
        profile = request.user.client_profile
        context.update({
            'name': profile.name,
            'avatar': profile.image.url if profile.image else None
        })

    client_profile = user.client_profile  
    confirmed_orders = Order.objects.filter(client=client_profile, status='confirmed', accept_client__isnull=True)
    active_orders = Order.objects.filter(client=client_profile, accept_client=True, end_order=None)
    end_orders = Order.objects.filter(client=client_profile, accept_client=True, end_order=True)
    reviews = Review.objects.filter(client=client_profile)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        client_profile.name = data.get('name') or client_profile.name
        client_profile.surname = data.get('surname') or client_profile.surname
        client_profile.surname2 = data.get('surname2') or client_profile.surname2
        client_profile.number = data.get('number') or client_profile.number
        client_profile.birthday = data.get('birthday') or client_profile.birthday
        client_profile.male = data.get('male') or client_profile.male
        if 'image' in files:
            client_profile.image = files['image']
        
        if 'delete-avatar' in data:
            client_profile.image = None
        client_profile.save()
        messages.success(request, 'Данные профиля успешно обновлены!')
        return redirect('profile')

    context.update({
        'confirmed_orders': confirmed_orders,
        'active_orders': active_orders,
        'end_orders': end_orders,
        'reviews': reviews,
        'stars_range': range(1, 6),
        'client': client_profile,
    })

    return render(request, 'profile.html', context)




# Детальная
def bus_details(request, bus_id):
    try:
        bus = Bus.objects.get(id=bus_id)
        response_data = {
            'name': bus.name,
            'image_url': bus.image.url if bus.image else None,  # Проверка URL изображения
        }
        return JsonResponse(response_data)
    except Bus.DoesNotExist:
        return JsonResponse({'error': 'Bus not found'}, status=404)

# Оставление отзыва
@csrf_protect
@login_required
def leave_review(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        stars = request.POST.get('stars')
        text = request.POST.get('text')
        order = Order.objects.get(id=order_id)

        if order.reviews.exists(): 
            return JsonResponse({'error': 'Вы уже оставили отзыв для этого заказа.'}, status=400)

        review = Review(
            client=request.user.client_profile,
            transport_company=order.bus.transport_company,
            stars=stars,
            text=text,
            order=order 
        )
        review.save()

        return JsonResponse({'message': 'Отзыв успешно отправлен'}, status=200)
    return JsonResponse({'error': 'Неверный запрос'}, status=400)

# Подтверждение заказа клиентом
@login_required
def update_accept_client(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, client=request.user.client_profile)
        accept_client = request.POST.get('accept_client') == 'true'
        order.accept_client = accept_client
        order.save()
        return redirect('profile')
    return JsonResponse({"error": "Метод не поддерживается."}, status=405)

# Страница компании
@login_required
def company_page(request):
    user = request.user
    if not user.is_company():
        return redirect('client')
    
    login_form = AuthenticationForm(data=request.POST or None)
    context = {'login_form': login_form}

    if request.user.is_authenticated:
        if request.user.is_company():
            profile = request.user.company_profile
            context.update({
                'name': profile.company_name,
                'avatar': profile.image.url if profile.image else None,
            })
            
            buses = Bus.objects.filter(transport_company=profile)
            avg_rating = Review.objects.filter(transport_company=profile).aggregate(
                avg_rating=Avg('stars'),
                reviews_count=Count('id')
            )
            
            context.update({
                'avg_rating': avg_rating['avg_rating'] if avg_rating['avg_rating'] else 'Нет отзывов',
                'reviews_count': avg_rating['reviews_count'],
            })
            
            features = Feature.objects.all()
            functionalitys = Functionality.objects.all()
            safetys = Safety.objects.all()
            context.update({
                'buses': buses,
                'features': features,
                'functionalitys': functionalitys,
                'safetys': safetys
            })
            
            orders = Order.objects.filter(bus__transport_company=profile).select_related('bus')
            pending_orders = orders.filter(status='pending')
            confirmed_orders = orders.filter(status='confirmed', accept_client=None and False)
            active_orders = orders.filter(accept_client=True, end_order=None)
            completed_orders = orders.filter(end_order=True)  

            context.update({
                'orders': orders,
                'pending_orders': pending_orders,
                'confirmed_orders': confirmed_orders,
                'active_orders': active_orders,
                'completed_orders': completed_orders,  
            })
           
            # Неотвеченные отзывы
            unanswered_reviews = Review.objects.filter(transport_company=profile, response__isnull=True)
            context.update({
                'unanswered_reviews': unanswered_reviews,
            })

            # Отвеченные отзывы
            answered_reviews = Review.objects.filter(transport_company=profile, response__isnull=False)
            context.update({
                'answered_reviews': answered_reviews,
            })
            
    return render(request, 'company.html', context)




# Ответ на отзыв компнии 
@login_required
def reply_to_review(request, review_id):
    if not request.user.is_company():
        return HttpResponseForbidden("Доступ запрещен")

    review = get_object_or_404(
        Review,
        id=review_id,
        order__bus__transport_company=request.user.company_profile
    )

    if request.method == 'POST':
        response_text = request.POST.get('response')
        if response_text:
            review.response = response_text
            review.save()
    return redirect('company')

# Ответ на заказ компании
@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        full_price = request.POST.get('full_price')  
        if status not in ['confirmed', 'rejected']:
            return JsonResponse({"error": "Неверный статус."}, status=400)
        if status == 'confirmed':
            if not full_price:
                return JsonResponse({"error": "Введите финальную цену."}, status=400)
            try:
                order.full_pirce = full_price
            except ValueError:
                return JsonResponse({"error": "Некорректное значение цены."}, status=400)
        order.status = status
        order.save()
        return redirect('company')
    return JsonResponse({"error": "Метод не поддерживается."}, status=405)


# Завершение заказа
@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST" and request.user.is_authenticated and request.user.is_company():
        action = request.POST.get('action')
        
        if action == "complete":
            order.end_order = True
            order.save()
        elif action == "cancel":
            order.end_order = False
            order.save()

    return redirect('company')


# Создание заказа
@login_required
@csrf_exempt
def calculate_cost(request, bus_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_date = data.get('order_date')
            description = data.get('description')

            if not order_date:
                return JsonResponse({"error": "Дата заказа не указана."}, status=400)

            order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
            bus = Bus.objects.get(id=bus_id)

            order = Order.objects.create(
                client=request.user.client_profile,
                bus=bus,
                date=order_date,
                status='pending',
                description=description
            )

            return JsonResponse({"message": "Ваш заказ успешно создан. Ожидайте подтверждения."}, status=200)
        except Bus.DoesNotExist:
            return JsonResponse({"error": "Автобус не найден."}, status=404)
        except ValueError as e:
            return JsonResponse({"error": f"Ошибка обработки даты: {e}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат данных."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)
    return JsonResponse({"error": "Метод не поддерживается."}, status=405)


# Редактирование автобуса
@login_required
def edit_bus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        price_per_day = request.POST.get('price_per_day')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        features_ids = request.POST.getlist('features')

        try:
            bus = Bus.objects.get(id=bus_id, transport_company=request.user.company_profile)
            bus.name = name
            bus.seats = seats
            bus.price_per_day = price_per_day
            bus.description = description
            if image:
                bus.image = image
            bus.features.set(features_ids)
            bus.save()
        except Bus.DoesNotExist:
            pass  # Handle error

        return redirect('company')

    return redirect('company')


# Удаление автобуса
@login_required
def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id, transport_company=request.user.company_profile)
    if request.method == 'POST':
        bus.delete()
        return redirect('company')
    return redirect('company')


# Добавление автобуса
@login_required
def add_bus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        price_per_day = request.POST.get('price_per_day')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        features_ids = request.POST.getlist('features')  
        functionality_ids = request.POST.getlist('functionality')  
        safety_ids = request.POST.getlist('safety') 
        bus_type = request.POST.get('type')  
        long_trips = request.POST.get('long_trips') == 'on'  
        transport_company = request.user.company_profile
        bus = Bus.objects.create(
            transport_company=transport_company,
            name=name,
            seats=seats,
            type=bus_type,  
            price_per_day=price_per_day,
            description=description,
            image=image,
            long_trips=long_trips,  
        )
        bus.features.set(features_ids)
        bus.functionality.set(functionality_ids)
        bus.safety.set(safety_ids)
        return redirect('company')

    return redirect('company')



# Регистрация
def register(request):
    client_form = ClientRegistrationForm(request.POST or None, request.FILES or None, prefix="client")
    company_form = CompanyRegistrationForm(request.POST or None, request.FILES or None, prefix="company")
    login_form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST':
        if 'register_client' in request.POST:
            if client_form.is_valid():
                user = client_form.save()
                login(request, user)
                return redirect('client')
            else:
                return render(request, 'registration/register.html', {
                    'client_form': client_form,
                    'company_form': company_form,
                    'login_form': login_form
                })


        elif 'register_company' in request.POST:
            if company_form.is_valid():
                user = company_form.save()
                login(request, user)
                return redirect('company')
            else:
                return render(request, 'registration/register.html', {
                    'client_form': client_form,
                    'company_form': company_form,
                    'login_form': login_form
                })

    return render(request, 'registration/register.html', {
        'client_form': client_form,
        'company_form': company_form,
        'login_form': login_form
    })







