from rest_framework import serializers
from apps.home.api.schemas import OurServiceApiListingApiSchemas, OurServicePointsApiListingApiSchemas
from apps.home.models import OurServices, OurServicesPoints
from apps.projects.models import EliminatingChallengesPoints, ProblemStatement, ProjectAminPoints, ProjectCaseStudy, ProjectCaseStudyBannerImage, ProjectCaseStudyBannerMultipleImages, ProjectCaseStudyImages, ProjectCaseStudyOutcomes, ProjectLiveUrls
from apps.home.models import TechStack

"""------------------------OUR SERVICE SEO LISTING----------------------------"""

class OurServiceSeoApiSchemas(serializers.ModelSerializer):
    service_points = serializers.SerializerMethodField('get_service_points')
    class Meta:
        model = OurServices
        fields = ['slug', 'id', 'title','full_name','button_titile','description_title', 'description', 'service_image', 'og_image', 'meta_image_title', 'meta_title', 'meta_description', 'meta_keyword','service_points']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
    def get_service_points(self,data):
        points = OurServicesPoints.objects.filter(service=data)
        service_points_serializer = OurServicePointsApiListingApiSchemas(points,many=True)
        if service_points_serializer:
            return service_points_serializer.data
        return []    

    
class ProjectCaseStudyApiListingApiSchemas(serializers.ModelSerializer):
    domain        = serializers.CharField(source="domain.title",allow_null=True)
    domain_id     = serializers.CharField(source="domain.slug",allow_null=True)
    service       = serializers.CharField(source="service.title",allow_null=True)
    service_id    = serializers.CharField(source="service.slug",allow_null=True)
    service_url    = serializers.CharField(source="service.url",allow_null=True)
    service_seo   = serializers.SerializerMethodField('get_our_service_seo')
    
    class Meta:
        model = ProjectCaseStudy
        fields = ['slug','id','url','project_tags','project_name','project_image','domain','domain_id','service_url','service_id','service','service_seo','is_project_casestudy']
        
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
    def get_our_service_seo(self,data):
        request=self.context['request']
        our_service_seo = OurServices.objects.filter(pk=data.service.id)
        our_service_seo_response =  OurServiceSeoApiSchemas(our_service_seo,many=True,context={'request': request})
        if our_service_seo_response:
            return our_service_seo_response.data
        return ''
    
    def get_our_service_bottom_section(self,data):
        request=self.context['request']
        our_service_seo = OurServices.objects.filter(pk=data.service.id)
        our_service_seo_response =  OurServiceApiListingApiSchemas(our_service_seo,many=True,context={'request': request})
        if our_service_seo_response:
            return our_service_seo_response.data
        return []





"""------------------------PROJECT MILTON SECTION----------------------------"""

class ProjectMilestoneApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudy
        fields = ['research','design_strategy','ui','backend_development','frontend_development','testing',]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
"""------------------------PROJECT TECH STACK----------------------------"""

class ProjectTechStackApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudy
        fields = ['front_technology','backend_technology','other_technology']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
"""------------------------PROJECT MODE OF FUNCTIONS----------------------------"""

class ProjectModeOfFunctionsApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudy
        fields = ['project_mode_of_functions']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

""" -------------------------PROJECT RELATED IMAGES-----------------------------"""

class ProjectCaseStudyRelatedImageApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudyImages
        fields = ['image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
""" -------------------------PROJECT URLS-----------------------------"""

class ProjectCaseStudyUrlsApiSchemas(serializers.ModelSerializer):
    # urls = serializers.CharField(source="Points",allow_null=True)
    class Meta:
        model = ProjectCaseStudyOutcomes
        fields = ['id','title','url']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
""" -------------------------PROJECT AIM -----------------------------"""

class ProjectAimApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectAminPoints
        fields = ['Points',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
""" -------------------------PROJECT PROBLEM STATEMENT -----------------------------"""

class ProjectProblemStatementApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProblemStatement
        fields = ['Points',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
""" -------------------------PROJECT Eliminating Challenges -----------------------------"""

class ProjectEliminatingChallengesApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = EliminatingChallengesPoints
        fields = ['Points',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

"""---------------------PROJECT DETAIL VIEW-----------------------"""

class ProjectCaseStudyDetailViewApiListingApiSchemas(serializers.ModelSerializer):
    domain                            = serializers.CharField(source="domain.title",allow_null=True)
    service                           = serializers.CharField(source="service.title",allow_null=True)
    service_id                        = serializers.CharField(source="service.slug",allow_null=True)
    project_screens                   = serializers.SerializerMethodField('get_project_screen_images')
    aims                              = serializers.SerializerMethodField('get_project_aim_points')
    project_problem_statements        = serializers.SerializerMethodField('get_project_problem_statement_points')
    project_eliminating_challenges    = serializers.SerializerMethodField('get_project_eliminating_challenges_points')
    project_milestones                = serializers.SerializerMethodField('get_project_milestone')
    tech_stack                        = serializers.SerializerMethodField('get_project_tech_stack')
    mode_of_functions                 = serializers.SerializerMethodField('get_project_mode_of_functions')
    the_out_comes_title               = serializers.CharField(source='web_url_title')
    the_out_comes_urls                = serializers.SerializerMethodField('get_project_url')
    service_seo                       = serializers.SerializerMethodField('get_our_service_seo')
    class Meta:
        model = ProjectCaseStudy
        fields = ['slug','id','url','project_image_banner','project_logo','banner_title','banner_description','project_name','project_image','service','service_id','domain','project_screens','aims','project_problem_statements','eliminating_challenges_description','project_eliminating_challenges',
                'project_milestones','tech_stack','mode_of_functions','the_out_comes_title','the_out_comes_urls','og_image','meta_image_title','meta_title','meta_description','meta_keyword','service_seo']
        
        
    def get_project_screen_images(self,data):
        request=self.context['request']
        projects_images = ProjectCaseStudyImages.objects.filter(project_case_study=data.id).order_by('id')
        projects_screen_images =  ProjectCaseStudyRelatedImageApiSchemas(projects_images,many=True,context={'request': request})
        if projects_screen_images:
            return projects_screen_images.data
        return ""
    
    def get_project_url(self,data):
        request=self.context['request']
        projects_url = ProjectCaseStudyOutcomes.objects.filter(project_id=data.id)
        projects_url =  ProjectCaseStudyUrlsApiSchemas(projects_url,many=True,context={'request': request})
        if projects_url:
            return projects_url.data
        return ""
    
    def get_project_aim_points(self,data):
        request=self.context['request']
        aim_points = ProjectAminPoints.objects.filter(project=data.id)
        aim_point_response =  ProjectAimApiListingApiSchemas(aim_points,many=True,context={'request': request})
        if aim_point_response:
            return aim_point_response.data
        return ""
    
    def get_project_problem_statement_points(self,data):
        request=self.context['request']
        project_problem_statement = ProblemStatement.objects.filter(project=data.id)
        project_problem_statement_response =  ProjectProblemStatementApiListingApiSchemas(project_problem_statement,many=True,context={'request': request})
        if project_problem_statement_response:
            return project_problem_statement_response.data
        return ""
    
    def get_project_eliminating_challenges_points(self,data):
        request=self.context['request']
        project_eliminating_challenges = EliminatingChallengesPoints.objects.filter(project=data.id)
        project_eliminating_challenges_response =  ProjectEliminatingChallengesApiListingApiSchemas(project_eliminating_challenges,many=True,context={'request': request})
        if project_eliminating_challenges_response:
            return project_eliminating_challenges_response.data
        return ""
    
    def get_project_milestone(self,data):
        request=self.context['request']
        project_milestone = ProjectCaseStudy.objects.filter(pk=data.id)
        project_milestone_response =  ProjectMilestoneApiListingApiSchemas(project_milestone,many=True,context={'request': request})
        if project_milestone_response:
            return project_milestone_response.data
        return ""
    
    def get_project_tech_stack(self,data):
        request=self.context['request']
        project_tech_stack = ProjectCaseStudy.objects.filter(pk=data.id)
        project_tech_stack_response =  ProjectTechStackApiListingApiSchemas(project_tech_stack,many=True,context={'request': request})
        if project_tech_stack_response:
            return project_tech_stack_response.data
        return ""
    
    def get_project_mode_of_functions(self,data):
        request=self.context['request']
        project_mode_of_functions = ProjectCaseStudy.objects.filter(pk=data.id)
        project_mode_of_functions_response =  ProjectModeOfFunctionsApiListingApiSchemas(project_mode_of_functions,many=True,context={'request': request})
        if project_mode_of_functions_response:
            return project_mode_of_functions_response.data
        return ""
    
    def get_our_service_seo(self,data):
        request=self.context['request']
        our_service_seo = OurServices.objects.filter(pk=data.service.id)
        our_service_seo_response =  OurServiceSeoApiSchemas(our_service_seo,many=True,context={'request': request})
        if our_service_seo_response:
            return our_service_seo_response.data
        return []
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


"""-----------------------PROJECT CASE STUDY BANNER SECTION-----------------------------------"""

class TechStackSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id','stack_title','stack_logo',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


class ProjectCaseStudyImagesApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudyBannerMultipleImages
        fields = ['uuid','image']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data



class ProjectCaseStudyBannerApiListingApiSchemas(serializers.ModelSerializer):
    front_technology    = serializers.CharField(source = 'project.front_technology',allow_null=True)
    backend_technology  = serializers.CharField(source = 'project.backend_technology',allow_null=True)
    
    project_name        = serializers.CharField(source = 'project.project_name',allow_null=True)
    project_url         = serializers.CharField(source = 'project.url',allow_null=True)
    project             = serializers.CharField(source = 'project.slug',allow_null=True)
    
    service_name        = serializers.CharField(source = 'project.service.title',allow_null=True)
    service_url         = serializers.CharField(source = 'project.service.url',allow_null=True)
    service             = serializers.CharField(source = 'project.service.slug',allow_null=True)
    banner_image        = serializers.SerializerMethodField('get_banner_images')
    
    tech_stack_technology = serializers.SerializerMethodField('get_tech_stack_technology')
    
    class Meta:
        model = ProjectCaseStudyBannerImage
        fields = ['id','project','project_name','project_url','title','url','description','front_technology','backend_technology','is_active','domain_title','service_name','service_url','service','banner_image','tech_stack_technology']
        
    def get_banner_images(self,data):
        request = self.context.get('request')
        images = ProjectCaseStudyBannerMultipleImages.objects.filter(project_case_study=data)
        image_serializer = ProjectCaseStudyImagesApiListingApiSchemas(images, many=True,context={'request': request})
        if image_serializer:
            return image_serializer.data
        return []
    
    def get_tech_stack_technology(self, data):
        request = self.context.get('request')
        
        tech_stack_data = {
            'tech_stack_1': None,
            'tech_stack_2': None,
        }
        
        if data.tech_stack_one:
            tech_stack_1 = TechStack.objects.filter(id=data.tech_stack_one.id)
            tech_stack_1_serializer = TechStackSerializerResponse(tech_stack_1, many=True, context={'request': request})
            tech_stack_data['tech_stack_1'] = tech_stack_1_serializer.data
        
        if data.tech_stack_two:
            tech_stack_2 = TechStack.objects.filter(id=data.tech_stack_two.id)
            tech_stack_2_serializer = TechStackSerializerResponse(tech_stack_2, many=True, context={'request': request})
            tech_stack_data['tech_stack_2'] = tech_stack_2_serializer.data
        
        # Convert 'null' to ''
        tech_stack_data['tech_stack_1'] = "" if tech_stack_data['tech_stack_1'] is None else tech_stack_data['tech_stack_1']
        tech_stack_data['tech_stack_2'] = "" if tech_stack_data['tech_stack_2'] is None else tech_stack_data['tech_stack_2']
        
        return tech_stack_data


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
    