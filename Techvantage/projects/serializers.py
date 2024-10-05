# serializers.py

from rest_framework import serializers
from .models import Project, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  # Include only essential fields


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # Read-only field to show tags in the response
    tag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False, help_text="List of tag names to be added to the project"
    )  # Write-only field to accept tag names

    class Meta:
        model = Project
        fields = ["id", "title", "user", "image", "content", "category", "contributors", "published_date", "tags", "tag_names"]

    def create(self, validated_data):
        # Extract 'tag_names' from validated data
        tag_names = validated_data.pop('tag_names', [])
        
        # Create the project
        project = Project.objects.create(**validated_data)

        # Create or get tags and associate them with the project
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)

        return project

    def update(self, instance, validated_data):
        # Extract 'tag_names' from validated data
        tag_names = validated_data.pop('tag_names', None)

        # Update the basic fields of the project
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update tags if 'tag_names' is provided
        if tag_names is not None:
            instance.tags.clear()  # Remove existing tags
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        instance.save()
        return instance
