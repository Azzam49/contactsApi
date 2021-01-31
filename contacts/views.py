from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import permissions


class ContactList(ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #saves the owner field , becuase its a ForeignKey field
    #it creates that instance by overriding the perform_create
    def perform_create(self,serializer):
        #owner will be the current logged in user
        serializer.save(owner=self.request.user)
    

    #get contacts of current logged in user by
    #overriding the get_queryset
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)



class ContactDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    # get the detial of a contact by id from url
    lookup_field = "id" # contacts/id #url config is path('<int:id>', ContactDetailView.as_view()),


    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)




    
