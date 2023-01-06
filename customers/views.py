import json
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View

from .models import MenuItem, OrderModel


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request,'customer/index.html')


class About(View):
    def get(self,request, *args, **kwargs):
        return render(request,'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        #pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        #return the template
        return render(request, 'customer/order.html',context)

    def post(self, request, *args, **kwargs):
        # Get input fields at the bottom of the order template
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'item': []
        }
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['item'].append(item_data)

            price=0
            item_ids=[]

        for item in order_items['item']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name = name,
            email = email,
            street = street,
            city = city,
            state = state,
            zip_code = zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to user
        body = ('Thank you for your order!  Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['item'],
            'price': price,
        }
        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)
        data = json.loads(request.body)
        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request,'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        return render(request, 'customer/menu.html', {'menu_items': menu_items})


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        menu_items = MenuItem.objects.filter(
            Q(name__contains=query) |
            Q(price__contains=query) |
            Q(description__contains=query)
        )
        return render(request, 'customer/menu.html', {'menu_items': menu_items})
