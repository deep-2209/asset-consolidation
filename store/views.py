from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import SupplierForm
import uuid
import io
from users.models import User
from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    Delivery
)
from .forms import (
    SupplierForm,
    BuyerForm,
    SeasonForm,
    DropForm,
    ProductForm,
    OrderForm,
    DeliveryForm
)
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
# from reportlab.pdfgen import canvas
from django.shortcuts import render



# class DashboardView(ListView):
#     model = Order
#     template_name = 'store/order_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['order'] = Order.objects.all().order_by('-id')
#         # context['order'] = Order.objects.filter(status__in=['approved', 'pending']).order_by('-id')
#         return context
    

@login_required(login_url='login')
def dashboard(request):
    # Query the database to get counts of each risk rating type
    very_low_count = Supplier.objects.filter(risk='Very Low').count()
    low_count = Supplier.objects.filter(risk='Low').count()
    moderate_count = Supplier.objects.filter(risk='Moderate').count()
    high_count = Supplier.objects.filter(risk='High').count()
    very_high_count = Supplier.objects.filter(risk='Very High').count()

    # Pass counts to the template context
    context = {
        'very_low_count': very_low_count,
        'low_count': low_count,
        'moderate_count': moderate_count,
        'high_count': high_count,
        'very_high_count': very_high_count,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def download_pdf(request):
    buyers = Buyer.objects.all()  # Fetch all Buyer objects from the database

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="investor_list.pdf"'

    # Create PDF
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    data = []

    # Add column headers to the data list
    data.append(['Name', 'Address', 'Email', 'Username', 'Investor Type', 'Tenure of Investment', 'Risk Tolerance', 'Investor Goals', 'Date'])

    # Add Buyer data to the data list
    for buyer in buyers:
        # Enable word wrapping for each cell
        name = buyer.name or ""
        address = buyer.address or ""
        email = buyer.user.email or ""
        username = buyer.user.username or ""
        investor_type = buyer.type or ""
        # rate_of_interest = buyer.interest or ""
        tenure_of_investment = buyer.tenure or ""
        risk_tolerance = buyer.risk or ""
        investor_goals = buyer.goals or ""
        date = buyer.created_date or ""

        data.append([name, address, email, username, investor_type, tenure_of_investment, risk_tolerance, investor_goals, date])

    # Create the table
    table = Table(data, repeatRows=1)  # Set repeatRows to ensure column headers are repeated on each page

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Align content vertically in the middle
                        ('WORDWRAP', (0, 0), (-1, -1), True)])  # Enable word wrapping

    table.setStyle(style)

    # Calculate column widths dynamically based on content length
    col_widths = []
    for col in range(len(data[0])):
        col_widths.append(max(len(str(row[col])) for row in data) * 10)  # Adjust the multiplier as needed

    # Ensure column widths match the number of columns
    table._argW = col_widths

    # Add table to the PDF
    pdf_table = [table]
    pdf.build(pdf_table)

    # Get PDF content and return response
    pdf_data = buffer.getvalue()
    buffer.close()
    response.write(pdf_data)
    return response


# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            local_part, domain_part = email.split('@')
            local_part = local_part.lower()
            domain_part = domain_part.lower()
            email = local_part + '@' + domain_part
            username = forms.cleaned_data['username']
            type = forms.cleaned_data['type']
            risk = forms.cleaned_data['risk']
            url = forms.cleaned_data['url']
            # interest = forms.cleaned_data['interest']
            tenure = forms.cleaned_data['tenure']
            supplier_id = str(uuid.uuid4().int)[:10]
            password = '1'
            retype_password = password
            if User.objects.filter(username=username).exists():
                print('Username already exists')
                return render(request, 'store/create_supplier.html', {'form': SupplierForm, 'error_message': 'Username already exists'})
            if password == retype_password:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_supplier=True
                )
                Supplier.objects.create(user=user, name=name, address=address, type=type, risk=risk, url=url, tenure=tenure, id=supplier_id)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_supplier.html', context)

@login_required(login_url='login')
def delete_supplier(request,pk):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return redirect('supplier-list')


@login_required(login_url='login')
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, supplier)
        if form.is_valid():
            supplier.name = form.cleaned_data['name']
            supplier.address = form.cleaned_data['address']
            supplier.user.email = form.cleaned_data['email']
            supplier.user.username = form.cleaned_data['username']
            supplier.risk = form.cleaned_data['risk']
            supplier.type = form.cleaned_data['type']
            supplier.url = form.cleaned_data['url']
            # supplier.interest = form.cleaned_data['interest']
            supplier.tenure = form.cleaned_data['tenure']
            supplier.save()
            supplier.user.save()
            return redirect('supplier-list')
    else:
        form = SupplierForm(initial={'name': supplier.name, 'address': supplier.address, 'email': supplier.user.email, 'username': supplier.user})
    return render(request, 'store/update_supplier.html', {'form': form})


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            local_part, domain_part = email.split('@')
            local_part = local_part.lower()
            domain_part = domain_part.lower()
            email = local_part + '@' + domain_part
            username = forms.cleaned_data['username']
            type = forms.cleaned_data['type']
            # interest = forms.cleaned_data['interest']
            tenure = forms.cleaned_data['tenure']
            risk = forms.cleaned_data['risk']
            goals = forms.cleaned_data['goals']
            buyer_id = str(uuid.uuid4().int)[:10]
            password = "1"
            retype_password = password
            if User.objects.filter(username=username).exists():
                print('Username already exists')
                return render(request, 'store/create_buyer.html', {'form': BuyerForm, 'error_message': 'Username already exists'})
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_buyer=True
                )
                Buyer.objects.create(user=user, name=name, address=address, type=type, tenure=tenure,risk=risk, goals=goals, id=buyer_id)
                return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_buyer.html', context)

@login_required(login_url='login')
def delete_buyer(request,pk):
    if request.method == 'POST':
        buyer = get_object_or_404(Buyer, pk=pk)
        buyer.delete()
        return redirect('buyer-list')


@login_required(login_url='login')
def update_buyer(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == 'POST':
        form = BuyerForm(request.POST, buyer)
        if form.is_valid():
            buyer.name = form.cleaned_data['name']
            buyer.address = form.cleaned_data['address']
            buyer.user.email = form.cleaned_data['email']
            buyer.user.username = form.cleaned_data['username']
            buyer.risk = form.cleaned_data['risk']
            buyer.type = form.cleaned_data['type']
            # buyer.interest = form.cleaned_data['interest']
            buyer.tenure = form.cleaned_data['tenure']
            buyer.goals = form.cleaned_data['goals']
            buyer.save()
            buyer.user.save()
            return redirect('buyer-list')
    else:
        form = BuyerForm(initial={'name': buyer.name, 'address': buyer.address, 'email': buyer.user.email, 'username': buyer.user})
    return render(request, 'store/update_buyer.html', {'form': form})



class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Season views
@login_required(login_url='login')
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('season-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_season.html', context)


@login_required(login_url='login')
def delete_season(request,pk):
    if request.method == 'POST':
        season = get_object_or_404(Season, pk=pk)
        season.delete()
        return redirect('season-list')


@login_required(login_url='login')
def update_season(request, pk):
    season = get_object_or_404(Season, pk=pk)
    if request.method == 'POST':
        form = SeasonForm(request.POST, season)
        if form.is_valid():
            season.name = form.cleaned_data['name']
            season.returnn = form.cleaned_data['returnn']
            season.description = form.cleaned_data['description']
            season.save()
            return redirect('season-list')
    else:
        form = SeasonForm(initial={'name': season.name, 'returnn': season.returnn, 'description': season.description})
    return render(request, 'store/update_season.html', {'form': form})

class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'


# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_drop.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/drop_list.html'
    context_object_name = 'drop'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_product.html', context)

@login_required(login_url='login')
def delete_product(request,pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product-list')


@login_required(login_url='login')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, product)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.classs = form.cleaned_data['classs']
            product.season = form.cleaned_data['season']
            product.sortno = form.cleaned_data['sortno']
            product.save()
            return redirect('product-list')
    else:
        form = ProductForm(initial={'name': product.name, 'classs': product.classs, 'season': product.season, 'sortno': product.sortno})
    return render(request, 'store/update_product.html', {'form': form})




class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            notes = forms.cleaned_data['notes']
            buyer = forms.cleaned_data['buyer']
            typee = forms.cleaned_data['typee']
            season = forms.cleaned_data['season']
            amt = forms.cleaned_data['amt']
            Order.objects.create(
                supplier=supplier,
                product=product,
                notes=notes,
                buyer=buyer,
                typee=typee,
                season=season,
                amt= amt,
                status='pending'
            )
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_order.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        context['order'] = Order.objects.filter(status__in=['approved', 'pending']).order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_delivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(status__in=['complete', 'decline']).order_by('-id')
        return context

