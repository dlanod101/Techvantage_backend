from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

from rest_framework.views import APIView

# Create your views here.
class JobListCreate(generics.ListCreateAPIView):
    """
    `POST` - Creates a new jobs
    `GET` - Lists out all existing jobs
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = "pk"


class JobFind(APIView):
    def get(self, request, format=None):
        """

        Available query parameters:

        1. `/jobs_find/?job_type=&lt; job_type &gt;` -- Finds all jobs with that job_type 
        2. `/jobs_find/?location=&lt; location &gt;` -- Finds all jobs with that location     
        3. `/jobs_find/?experience=&lt; experience &gt;` -- Finds all jobs with that experience
        4. `/jobs_find/` -- Displays all available jobs 
        """ 
        #Gets title from the query parameter
        job_type = request.query_params.get("job_type", "")

        location = request.query_params.get("location", "")

        experience = request.query_params.get("experience", "")

        if job_type:
            job = Job.objects.filter(job_type__icontains=job_type)
        
        if location:
            job = Job.objects.filter(location__icontains=location)

        if experience:
            job = Job.objects.filter(experience__icontains=experience)
        
        else:
            job = Job.objects.all()

        serializer = JobSerializer(job, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
