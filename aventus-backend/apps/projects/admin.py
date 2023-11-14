from django.contrib import admin

from apps.projects.models import EliminatingChallengesPoints, ProjectCaseStudy, ProjectCaseStudyBannerMultipleImages,ProjectCaseStudyImages,ProjectAminPoints,ProblemStatement,ProjectCaseStudyBannerImage, ProjectCaseStudyOutcomes

# Register your models here.
admin.site.register(ProjectCaseStudy)
admin.site.register(ProjectCaseStudyImages)
admin.site.register(ProjectAminPoints)
admin.site.register(ProblemStatement)
admin.site.register(EliminatingChallengesPoints)
admin.site.register(ProjectCaseStudyBannerImage)
admin.site.register(ProjectCaseStudyBannerMultipleImages)
admin.site.register(ProjectCaseStudyOutcomes)