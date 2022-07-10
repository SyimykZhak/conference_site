
from django.contrib import messages
from django.shortcuts import redirect,HttpResponse
from django.views.generic import DetailView, View,ListView
from django.db.models import Sum
from .forms import UserForm,UploadFileForm
from .models import Conference, Register
from django.shortcuts import render



class MainListView(ListView):
    model = Conference
    template_name ='core/main.html'
    context_object_name = "conferences"
    queryset = Conference.objects.filter(draft = False)

  
# class ConferenceDetail(DetailView):    
#     model = Conference
#     template_name = 'core/conference.html'
#     context_object_name = "conference"
#     slug_field = "url"



    
    



def confrence(request,url):
    try:
        conference_object = Conference.objects.get(url=url)
        registers = Register.objects.filter(conference__url=url).select_related("conference")
        registers_count = conference_object.tickets - registers.count()
        if registers_count == 0 or registers_count < 0:
            messages.success(request, "К сожалению мест не осталось!!!")
        context = { 
            'conference': conference_object, 
            # "registers": registers_count,
            }
        return render(request, 'core/conference.html', context)
    except Conference.DoesNotExist as e:
        return HttpResponse('Not found karoche: {e}',status = 404)


class RegisterView(View):
    def post(self, request,pk):
        conference_object = Conference.objects.get(id=pk)
        registers = Register.objects.filter(conference__id=pk).select_related("conference")
        registers_count = conference_object.tickets - registers.count()
        if registers_count == 0 or registers_count < 0:
            return HttpResponse('Билетов не осталось',status=404)
        form = UserForm(request.POST)
        conference = Conference.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.conference = conference
            form.save()
        return redirect("/")

class WorkView(View):
    def post(self, request,pk):
        form = UploadFileForm(request.POST, request.FILES)
        conference = Conference.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.conference = conference
            form.save()
        return redirect("/")


def example(request):
    data = Conference.objects.all().aggregate(data=Sum('raiting_count'))
    return render(request, 'core/index.html', {"data": data})
