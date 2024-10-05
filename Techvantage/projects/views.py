from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Project, Tag
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from django.db.models import Q  # Import Q object for complex queries

# Create your views here.

class ProjectListCreate(generics.ListCreateAPIView):
    """
    `POST` - Creates a new project
    `GET` - Lists out all existing projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "pk"


class ProjectFind(APIView):
    def get(self, request, format=None):
        """
        Available query parameters:
        
        1. `/projects_find/?category=<category>` -- Finds all projects with that category
        2. `/projects_find/?tag=<tag>` -- Finds all projects with that tag
        3. `/projects_find/?contributors=<contributors>` -- Finds all projects with that contributor
        4. `/projects_find/` -- Displays all available projects

        """
        # Retrieve query parameters
        tag = request.query_params.get("tag", "")
        category = request.query_params.get("category", "")
        contributors = request.query_params.get("contributors", "")

        # Build query filters using Q objects
        filters = Q()
        
        if category:
            filters &= Q(category__icontains=category)  # Filter by category (case insensitive)

        if tag:
            filters &= Q(tags__name__icontains=tag)  # Assuming the 'tags' field is a many-to-many relation

        if contributors:
            filters &= Q(contributors__icontains=contributors)  # Filter by contributors (case insensitive)

        # Apply filters if there are any, otherwise return all projects
        project = Project.objects.filter(filters) if filters else Project.objects.all()

        # Serialize the filtered projects and return the response
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
