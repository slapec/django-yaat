from django.shortcuts import render


def model_example(request):
    return render(request, 'yaat_examples/model_example.html')
