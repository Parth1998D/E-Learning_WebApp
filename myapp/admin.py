from django.contrib import admin
from .models import Topic, Course, Student, Order

# Register your models here.
# admin.site.register(Topic)
# admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    inlines = [
        CourseInline,
    ]


admin.site.register(Topic, TopicAdmin)


def reduce_price(modeladmin, request, queryset):
    for course in queryset:
        course.price = 90 * course.price / 100
        course.save()
    reduce_price.short_description = 'Reduce price'


class CourseAdmin(admin.ModelAdmin):
    actions = [reduce_price]


admin.site.register(Course, CourseAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','level','registered_courses')

    def level(self, obj):
        levels = Order.objects.filter(student=obj)
        count = 0
        list_of_levels = ''
        for level in levels:
            list_of_levels += str(level.levels)
            count += 1
            if count < len(levels):
                list_of_levels += ", "
        return list_of_levels

    def registered_courses(self, obj):
        courses = Order.objects.filter(student=obj)
        list_of_course = ""
        count = 0
        for course in courses:
            list_of_course += course.course.name
            count +=1
            if count < len(courses):
                list_of_course += ", "
        return list_of_course


admin.site.register(Student, StudentAdmin)