# -*- coding: utf-8 -*-

from django.shortcuts import render

def about(request):
    return render(request, 'frontend/about/about.html')
