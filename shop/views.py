from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as auth_logout
import json
from django.http import JsonResponse


# Create your views here.
def Homepage(request):
    products=Products.objects.filter(Trending_product=1)
    return render(request,"shop/index.html",{"products":products})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user  is not None:
                login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name and Password")
                return redirect("/login")
        return render(request,"shop/login.html")
     

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Logib Now...!")
            return redirect('/login')
        
    return render(request,"shop/register.html",{"form":form})
    
def Collections(request):
    catagory=Catagory.objects.filter(Status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})   
'''
def Collectionsview(request, name):
    if(Catagory.objects.filter(Catagory_Name=name,Status=0)):
        products = Products.objects.filter(Catagory=name)
        return render(request,"shop/products/index.html",{"products":products})   
    else:
        messages.warning(request,"No Such catagory Found")
        return redirect('collections')
'''
def Collectionsview(request, name):
    try:
        # Fetch the category object using the name provided in the URL
        catagory = Catagory.objects.get(Catagory_Name=name, Status=0)
        
        # Filter products that belong to this category
        products = Products.objects.filter(Catagory=catagory)
        
        return render(request, "shop/products/index.html", {"products": products,"Catagory_Name":name})
    
    except Catagory.DoesNotExist:
        messages.warning(request, "No Such Category Found")
        return redirect('collections') 

def product_details(request,cname,pname):
    if(Catagory.objects.filter(Catagory_Name=cname,Status=0)):
        if(Products.objects.filter(Product_Name=pname,Status=0)):
            products=Products.objects.filter(Product_Name=pname,Status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No Such Catagory Faund")
            return redirect('collections') 
    else:
        messages.error(request,"No Such Catagory Faund")
        return redirect('collections') 

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, Products
from django.contrib.auth.decorators import login_required

@login_required

def addCart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        # Fetch the product from the database
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return redirect('product_not_found')  # Redirect to an error page if product not found

        # Calculate total amount (quantity * product price)
        total_amount = product.Selling_price * quantity

        # Add the product to cart (or update the existing cart entry)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'product_qty': quantity, 'product_amount': total_amount}
        )

        if not created:
            # If cart item exists, update the quantity and amount
            cart_item.product_qty += quantity
            cart_item.product_amount = cart_item.product_qty * product.Selling_price
            cart_item.save()

        # Redirect back to the product detail page or cart page
        return redirect('cart')  # Assuming you have a cart page to display items in the cart

    return redirect('home')  # Redirect to home page if the method is not POST


from django.shortcuts import render
from .models import Cart


def cart_view(request):
    # Assuming you filter the cart by the currently logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Cart

import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.utils import timezone
from .models import Cart

def download_cart_pdf(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to be logged in to download cart details.")
        return redirect('login')

    # Fetch cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)

    # Create a BytesIO buffer to hold the PDF data
    buffer = io.BytesIO()
    
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.textColor = colors.darkblue

    header_style = styles['Heading2']
    header_style.fontSize = 14
    header_style.textColor = colors.black

    data_style = styles['Normal']
    data_style.fontSize = 10

    # Title
    elements.append(Paragraph("Cart Details", title_style))

    # Date and time
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Purchase on: {now}", data_style))
    elements.append(Paragraph("<br/><br/>", data_style))  # Add space between date and table

    # Table data
    table_data = [
        ["Product Name", "Purchase Date", "Quantity", "Price", "Total"]
    ]

    for item in cart_items:
        table_data.append([
            item.product.Product_Name,
            item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            item.product_qty,
            f"Rs {item.product.Selling_price}",
            f"Rs {item.product_amount}"
        ])

    # Create table with styles
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    # Get PDF data from buffer
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    # Return PDF response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cart_details.pdf"'
    return response
