import re
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def sendEmail2(request):
    try:
        checked_res_list = request.POST.getlist('checks')
        inputReceiver = request.POST['inputReceiver']
        inputTitle = request.POST['inputTitle']
        inputContent = request.POST['inputContent']
        restaurants = []
        for checked_res_id in checked_res_list:
            restaurants.append(Restaurant.objects.get(id=checked_res_id))

        content = {'inputContent' : inputContent, 'restaurants' : restaurants}
        msg_html = render_to_string('shareRes/email_format.html', content)

        msg = EmailMessage(subject = inputTitle, body = msg_html, from_email="traumes84@gmail.com", bcc=inputReceiver.split(','))
        msg.content_subtype = 'html'
        msg.send()
        return render(request, 'shareRes/sendSuccess.html')
    
    except :
        return render(request, 'shareRes/sendFail.html')


def sendEmail(request):
    checked_res_list = request.POST.getlist('checks')
    inputReceiver = request.POST['inputReceiver']
    inputTitle = request.POST['inputTitle']
    inputContent = request.POST['inputContent']
    print(checked_res_list, "/", inputReceiver, "/", inputTitle, "/", inputContent)
    
    mail_html = "<html><body>"
    mail_html += "<h1> 맛집 공유 </h1>"
    mail_html += "<p>"+inputContent+"<br>"
    mail_html += "발신자님께서 공유하신 맛집은 다음과 같습니다.</p>"
    
    for checked_res_id in checked_res_list:
        restaurant = Restaurant.objects.get(id = checked_res_id)
        mail_html += "<h2>"+restaurant.restaurant_name+"</h3>"
        mail_html += "<h4>* 관련 링크 </h4>"+"<p>"+restaurant.restaurant_link+"</p><br>"
        mail_html += "<h4>* 상세 내용 </h4>"+"<p>"+restaurant.restaurant_content+"</p><br>"
        mail_html += "<h4>* 관련 키워드</h4>"+"<p>"+restaurant.restaurant_keyword+"</p><br>"
        mail_html += "<br>"
        print(mail_html)
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("traumes84@gmail.com","kafka1984!")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = inputTitle
        msg['From'] = "traumes84@gmail.com"
        msg['To'] = inputReceiver
        mail_html = MIMEText(mail_html,'html')
        msg.attach(mail_html)
        print(msg['To'], type(msg['To']))
        server.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
        server.quit()

    return render(request, 'shareRes/sendSuccess.html')
    #return HttpResponseRedirect(reverse('index'))
    #return HttpResponse("센드이메일")

def index(request):
    #return HttpResponse("index")
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()    
    content = {'categories' : categories, 'restaurants': restaurants}
    return render(request, 'shareRes/index.html', content)

def restaurantDetail(request, res_id):
    #return HttpResponse("restaurantDetail")
    restaurant = Restaurant.objects.get(id = res_id)
    content = {'restaurant': restaurant}
    return render(request, 'shareRes/restaurantDetail.html', content)

def restaurantCreate(request):
    categories = Category.objects.all()
    content = {'categories': categories}
    #return HttpResponse("restaurantCreate")   
    return render(request, 'shareRes/restaurantCreate.html', content)   

def restaurantUpdate(request, res_id):
    categories = Category.objects.all()
    restaurant = Restaurant.objects.get(id = res_id)
    content = {'categories' : categories, 'restaurant': restaurant}
    return render(request, 'shareRes/restaurantUpdate.html', content)

def delete_restaurant(request):
    res_id = request.POST['resId']
    restaurant = Restaurant.objects.get(id = res_id)
    restaurant.delete()
    return HttpResponseRedirect(reverse('index'))
    
def Update_restaurant(request):
    resId = request.POST['resId']
    change_category_id = request.POST['resCategory']
    change_category = Category.objects.get(id=change_category_id)
    change_name = request.POST['resTitle']
    change_link = request.POST['resLink']
    change_content = request.POST['resContent']
    change_keyword = request.POST['resLoc']
    before_restaurant = Restaurant.objects.get(id = resId)
    before_restaurant.category = change_category
    before_restaurant.restaurant_name = change_name
    before_restaurant.restaurant_link = change_link
    before_restaurant.restaurant_content = change_content
    before_restaurant.restaurant_keyword = change_keyword
    before_restaurant.save()
    return HttpResponseRedirect(reverse('resDetailPage', kwargs={'res_id':resId}))

def Create_restaurant(request):
    category_id = request.POST['resCategory']
    category = Category.objects.get(id = category_id)
    name = request.POST['resTitle']
    link = request.POST['resLink']
    content = request.POST['resContent']
    keyword = request.POST['resLoc']
    new_res = Restaurant(category = category, restaurant_name = name, restaurant_link = link, restaurant_content = content, restaurant_keyword = keyword)
    new_res.save()
    return HttpResponseRedirect(reverse('index'))

def categoryCreate(request):
    #return HttpResponse("categoryCreate")
    categories = Category.objects.all()
    content = {'categories':categories}
    return render(request, 'shareRes/categoryCreate.html', content)

def Create_category(request):
    category_name = request.POST['categoryName']
    new_category = Category(category_name = category_name)
    new_category.save()
    return HttpResponseRedirect(reverse('index'))    
    #return HttpResponse("여기서 category Create 기능을 구현할거야.")

def Delete_category(request):
    category_id = request.POST['categoryId']
    delete_category = Category.objects.get(id=category_id)
    delete_category.delete()
    return HttpResponseRedirect(reverse('cateCreatePage'))