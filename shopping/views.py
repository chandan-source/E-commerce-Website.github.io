from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse,Http404
from .forms import *
import requests
import json
from datetime import date,timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
sizelist=[["xs","xs"],
      ["s","s"],
      ["m","m"],
      ["l","l"],
      ["xl","xl"]]
def my_cart(user=None):
    cartlist=[]
    if user.is_authenticated:
        cart=Cart.objects.filter(usr=user)
        cartlist=cart[:2]
        return cartlist

def home(request):
    allcat=category.objects.all()
    allsubcat=subcategory.objects.all()
    top3subcategory=allsubcat[0:3]
    allproduct=product.objects.all()
    top8product=allproduct[0:8]
    d={"allcat":allcat,"mycart":my_cart(request.user),"top3subcategory":top3subcategory,"top8product":top8product}
    return render(request,'index.html',d)
def contactus(request):
    allcat = category.objects.all()
    d = {"allcat": allcat,"mycart":my_cart(request.user)}
    return render(request,'contact.html',d)
def aboutus(request):
    allcat = category.objects.all()
    d = {"allcat": allcat,"mycart":my_cart(request.user)}
    return render(request,'about.html',d)
def logIn(request):
    allcat = category.objects.all()
    error=False
    if request.method=="POST":
        dic=request.POST
        u=dic['usr']
        p=dic['pwd']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('home')
        else:
            error=True

    d = {"allcat": allcat,"error":error,"mycart":my_cart(request.user)}
    return render(request,'login.html',d)
def signup(request):
    allcat = category.objects.all()
    error=False
    if request.method=='POST':
        dic=request.POST
        f=dic['fname']
        l=dic['lname']
        u=dic['usr']
        e=dic['email']
        p=dic['pwd']
        m=dic['mob']
        a=dic['address']
        i=request.FILES['image']
        userdata=User.objects.filter(username=u)
        if not userdata:
            user=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            user_detail.objects.create(usr=user,mobile=m,img=i,address=a)
            return redirect('home')
        else:
            error=True
    d = {"allcat": allcat,"error":error,"mycart":my_cart(request.user)}
    return render(request,'signin.html',d)
def Logout(request):
    logout(request)
    return redirect('home')
def shop(request,sid):
    allcat = category.objects.all()
    subcatdata = subcategory.objects.get(id=sid)
    allpro = product.objects.filter(subcat=subcatdata)
    othersubcat = subcategory.objects.filter(cat=subcatdata.cat)
    paginator = Paginator(allpro,3)
    page=request.GET.get('page',1)
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages)

    d = {"allcat":allcat,"allpro":products,"othersubcat":othersubcat,"mycart":my_cart(request.user)}
    return render(request,'shop.html',d)
def Product(request,pid):
    allcat=category.objects.all()
    prodetail=product.objects.get(id=pid)
    sizelist=[]
    if prodetail.size:
        sizelist = prodetail.size.split(',')
    subcata=prodetail.subcat
    related_product=product.objects.filter(subcat=subcata)[0:5]
    d={"allcat":allcat,"prodetail":prodetail,"related_product":related_product,"sizelist":sizelist,"mycart":my_cart(request.user)}
    return render(request,'product-detail.html',d)
def addtocart(request,pid):
    allcat = category.objects.all()
    prodata=product.objects.get(id=pid)
    user=request.user
    if request.method=="POST":
        dic=request.POST
        q=dic['quantity']
        s=''
        if prodata.size:
            s=dic['size']
        total=int(q)*int(prodata.price)
        Cart.objects.create(usr=user,pro=prodata,quatity=q,total_price=total,size=s)
        return redirect('home')
def mycart(request):
    cartdata=Cart.objects.filter(usr=request.user)
    total=0
    for i in cartdata:
        total=total+i.total_price
    allcat=category.objects.all()
    d={"allcat":allcat,"mycart":my_cart(request.user),"cartdata":cartdata,"total":total}
    return render(request,'cart.html',d)
def remove_pro_from_cart(request,cid):
    delete_data=Cart.objects.get(id=cid)
    delete_data.delete()
    return redirect('mycart')

#def Send_mail(user,order_id):
    #orderdata=order_product.objects.get(id=order_id)
    #alldata=order_product_detail.objects.filter(order_detail=orderdata)
    #total_p=0;
    #for i in alldata:
        #total_p=total_p+i.totalprice
    #name=user.first_name
    #to_email=user.email
    #from_email = settings.EMAIL_HOST_USER
    #subject='confirmation mail'
    #msg=EmailMultiAlternatives(subject,'',from_email,[to_email])
    #d={"name":name,"total_p":total_p,"alldata":alldata}
    #html=get_template('mail.html').render(d)
    #msg.attach_alternative(html,'text/html')
    #msg.send()
def payment_check(request,order_id):
    orderdata=order_product.objects.get(id=order_id)
    payment_id=orderdata.payment_id
    url="https://www.instamojo.com/api/1.1/payment-requests/"+str(payment_id)+"/"
    response=requests.get(url,headers=headers)
    res=response.text
    y=json.loads(res)
    print(y)
    status=y['payment_request']['status']
    d={"orderdata":orderdata,"status":status}
    if status=='Completed':
        user=request.user
        #Send_mail(user,order_id)
        orderdata.payment_status='done'
        orderdata.save()
        order_detail_data=order_product_detail.objects.filter(order_detail=orderdata)
        for i in order_detail_data:
            i.status="order confirmed"
            i.save()
            #prodata=product.objects.get(id=i.pro.id)
            #q=i.quantity
            #prodata.stock-=q
            cartdata=Cart.objects.filter(usr=request.user,pro=i.pro)
            cartdata.delete()
            return redirect('home')
            #return redirect(request,'confirmation.html',d)
    else:
        return redirect(request,'confirmation.html',d)


headers = {"X-Api-Key": "70b5674bd028c4ef8531e6b6ca44479e", "X-Auth-Token": "e725a6662c8870638c820cdedb22dea8"}
def payment(user,amount,order_id):
    import requests
    import json


    payload = {
        'purpose': 'product payment',
        'amount': '10',
        'buyer_name': user.username,
        'email': user.email,
        'phone': +917007138811,
        'send_email': True,
        'send_sms': True,
        'redirect_url': "http://127.0.0.1:8000/payment_check/"+str(order_id)+"/"


    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
    res=response.text
    y=json.loads(res)
    print("result..." )
    print(y)
    payment_id=y['payment_request']['id']
    long_url=y['payment_request']['longurl']
    return payment_id,long_url





def checkout(request,cid):
    allcat=category.objects.all
    cart=Cart.objects.get(id=cid)
    form = OrderForm()
    if cid!='All':
        cartdata=Cart.objects.filter(id=cid)
    elif cid=='All':
        cartdata=Cart.objects.filter(usr=request.user)
    totalpayamount=0
    for i in cartdata:
        totalpayamount+=i.pro.price
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            data=form.save()
            data.amount=totalpayamount
            import random
            ran=random.randint(100000,999999)
            data.order_id=ran
            data.order_date=date.today()
            data.usr=request.user
            data.save()

            payid,longurl=payment(request.user,totalpayamount,data.id)
            data.payment_id=payid
            data.save()
            exp_date=date.today()+timedelta(5)
            for i in cartdata:
                order_product_detail.objects.create(order_detail=data, pro=i.pro, quantity=i.quatity,totalprice=i.pro.price,expected_date=exp_date)
            return redirect(longurl)
    d={"allcat":allcat,"mycart":my_cart(request.user),"form":form,"cart":cart}
    return render(request,'checkout.html',d)

def user_dashboard(request,type):
    allcat = category.objects.all
    c1=''
    c2=''
    c3=''
    c4=''
    AllOrder = []
    Pending_Order = []
    checkout_detail = []
    profile_detail = []
    order_data = order_product.objects.filter(usr=request.user)
    for checkout in order_data:
        alldata = order_product_detail.objects.filter(order_detail=checkout)
        for i in alldata:
            if i.status == 'delivered':
                AllOrder.append(i)
            else:
                Pending_Order.append(i)

    if type == 'AllOrder':
        c1 = 'active'

    elif type == 'PendingOrder':
        c2 = 'active'

    elif type == 'AddressList':
        c3 = 'active'
        checkout_detail = order_product.objects.filter(usr=request.user)

    elif type == 'Profile':
        profile_detail = user_detail.objects.filter(usr=request.user).first()
        c4 = 'active'
    else:
        raise Http404()
    d = {"type": type, "class1": c1, "class2": c2, "class3": c3, "class4": c4
        , "allorder": AllOrder, "pending_order": Pending_Order, "checkout_detail": checkout_detail,
         "profile_detail": profile_detail,"allcat": allcat,"mycart":my_cart(request.user)}
    return render(request, 'dashboard.html', d)





def track_order(request,oid):
    allcat=category.objects.all()
    orderdata=order_product_detail.objects.get(id=oid)
    d={"orderdata":orderdata,"allcat": allcat,"mycart":my_cart(request.user)}
    return render(request,'track.html',d)

def add_product(request):
    form=add_product_form()
    allcat=category.objects.all()
    subcat=subcategory.objects.all()
    if request.method == 'POST':
        form=add_product_form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save()
            return redirect('home')
    d={"form":form,"subcat":subcat,"allcat": allcat,"mycart":my_cart(request.user)}

    return render(request,'add_product.html',d)

def add_category(request):
    form=add_category_form()
    allcat=category.objects.all()
    if request.method=='POST':
        form=add_category_form(request.POST)
        if form.is_valid():
            data=form.save()
            return redirect('home')
    d={"form":form,"allcat": allcat,"mycart":my_cart(request.user)}

    return render(request,'add_category.html',d)

def add_subcategory(request):
    allcat=category.objects.all()
    form=add_subcategory_form()
    if request.method=='POST':
        form=add_subcategory_form(request.POST)
        if form.is_valid():
            data=form.save()
            return redirect('home')
    d={"form":form,"allcat": allcat,"mycart":my_cart(request.user)}

    return render(request,'add_subcategory.html',d)
def order_detail(request,type):
    allcat=category.objects.all()
    completed_order=[]
    pending_order=[]
    alldata=order_product_detail.objects.all()
    for i in alldata:
        if(i.status=='delivered'):
            completed_order.append(i)
        else:
            pending_order.append(i)
    d={"type":type,"completed_order":completed_order,"pending_order":pending_order,"allcat": allcat,"mycart":my_cart(request.user)}


    return render(request,'order_detail.html',d)
def change_status(request,order_id):
    allcat=category.objects.all()
    status = ["order_confirmed",'shipped',"out_for_delivery","delivered"]
    orderdata=order_product_detail.objects.get(id=order_id)
    dropdown=[]
    ind=status.index(orderdata.status)
    dropdown=status[ind+1:]
    if request.method=='POST':
        S=request.POST['status']
        orderdata.status=S;
        orderdata.save()
        return redirect('home')
    d={"dropdown":dropdown,"allcat": allcat,"mycart":my_cart(request.user)}

    return render(request,'change_status.html',d)
def edit(request,type,eid):
    allcat=category.objects.all()
    if type=='product':
        prodata = product.objects.get(id=eid)
        form = add_product_form(instance=prodata)
        d = {"type": type, "form": form,"prodata":prodata}
        if request.method == "POST":
            form = add_product_form(request.POST or None, request.FILES or None, instance=prodata)
            if form.is_valid():
                data = form.save()
            return redirect('home')
    elif type=='category':
        catdata=category.objects.get(id=eid)
        form=add_category_form(instance=catdata)
        d = {"type": type, "form": form,"allcat": allcat,"mycart":my_cart(request.user)}
        if request.method == "POST":
            form = add_category_form(request.POST or None, instance=catdata)
            if form.is_valid():
                data = form.save()
                return redirect('home')

    elif type=='subcategory':
        subcatdata=subcategory.objects.get(id=eid)
        form=add_subcategory_form(instance=subcatdata)
        d = {"type": type, "form": form}
        if request.method == "POST":
            form = add_subcategory_form(request.POST or None, instance=subcatdata)
            if form.is_valid():
                data = form.save()
                return redirect('home')



    return render(request,'edit.html',d)
def delete(request,type,did):
    if type == 'category':
        catdata=category.objects.get(id=did)
        catdata.delete()
    elif type == 'subcategory':
        subcatdata=subcategory.objects.get(id=did)
        subcatdata.delete()
    elif type == 'product':
        prodata=product.objects.get(id=did)
        prodata.delete()
    return redirect(home)




