from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
