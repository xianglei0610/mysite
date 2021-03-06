
# Register your models here.

from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

from .resources import UserResource
from .models import User, Teacher, CourseRecord, VipProduct,VipProductOrder
from .forms import UserForm, TeacherForm, VipProductForm, VipProductOrderForm

from django.utils.text import capfirst


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner



@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        "show_save_as_new": False,
        "show_save_and_add_another": False,
        "show_save_and_continue": False,
    })
    return ctx


class UserAdmin(ImportExportActionModelAdmin):
    form = UserForm
    resource_class = UserResource
    list_display = ('id', 'name', 'telephone', 'gender', 'age','id_card', 'remark', 'create_time','update_time',)
    list_display_links = ('id', 'name', 'telephone')
    search_fields = ('name', 'telephone',)
    list_per_page = 15
    ordering = ['-id']
    save_as_continue = False


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('id', 'name', 'telephone', 'gender', 'status', 'remark', 'create_time','update_time',)
    list_display_links = ('id', 'name', 'telephone')
    search_fields = ('name', 'telephone',)
    list_per_page = 15
    ordering = ['-id']
    save_as_continue = False


class VipProductAdmin(admin.ModelAdmin):
    form = VipProductForm
    list_display = ('id', 'name', 'amount', 'count', 'remark', 'create_time','update_time',)
    list_display_links = ('id', 'name', )
    search_fields = ('name',)
    list_per_page = 15
    ordering = ['-id']


class VipProductOrderAdmin(admin.ModelAdmin):
    form = VipProductOrderForm
    list_display = ('id', 'product_id', 'user_id', 'price','count', 'unit_price','remain_count','use_count', 'state','start_date','deadline_date','create_time','update_time', 'remark',)
    list_display_links = ('id', 'user_id', 'product_id')
    search_fields = ('user_id__telephone','user_id__name','product_id__name')
    list_filter = ('user_id__name','user_id__telephone','state')
    actions = ['delete_selected', 'commit_check']
    fields = ('product_id', 'user_id', 'price', 'count','start_date','deadline_date','remain_count','state', 'remark')
    list_per_page = 15
    ordering = ['-id']
    autocomplete_fields = ('user_id',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.state == 2:
            return ["user_id", "product_id", 'price','count','state','unit_price','remain_count']
        else:
            return ['state','unit_price','remain_count']

    def delete_selected(self, request, queryset):
        count = 0
        if queryset.filter(state=2).count()>0:
            msg = '???????????????????????????????????????????????????????????????'
            self.message_user(request, msg, level=messages.ERROR)
        else:
            for i in queryset:
                if i.state == 1:
                    i.delete()
                    count += 1
            if count > 0:
                msg = '???????????????{}???????????????'.format(count)
            else:
                msg = '?????????????????????'
            self.message_user(request, msg, level=messages.SUCCESS if count>0 else messages.WARNING)

    delete_selected.short_description = '???????????????'

    # ??????
    def commit_check(self,request,queryset):
        count = 0
        if queryset.filter(state=2).count() > 0:
            msg = '??????????????????????????????????????????????????????????????????'
            self.message_user(request, msg, level=messages.ERROR)
        else:
            for i in queryset:
                if i.state == 1:
                    i.state = 2
                    i.remain_count = i.count
                    i.save()
                    count += 1
            if count > 0:
                msg = '???????????????{}?????????'.format(count)
            else:
                msg = '?????????????????????'
            self.message_user(request, msg, level=messages.SUCCESS if count>0 else messages.WARNING)
    commit_check.short_description = u"????????????"
    commit_check.confirm = '????????????????????????'
    commit_check.icon = 'fas fa-check'
    commit_check.type = 'success'


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_order_id','unit_price', 'user_name','teacher_id', 'reservation_date','state', 'start_date','end_date', 'create_time','update_time', 'remark', 'print_record', )
    list_display_links = ('id', 'product_order_id', 'teacher_id')
    #search_fields = ('start_date', 'product_order_id', 'teacher_id' )
    list_filter = ('product_order_id__product_id__name','product_order_id__user_id__name','product_order_id__user_id__telephone','teacher_id__name','teacher_id__telephone', 'state','start_date')
    actions = ['delete_selected', "commit_check", 'commit_cancel']
    readonly_fields = ['state']
    fields = ('product_order_id', 'teacher_id', 'reservation_date', 'start_date', 'end_date','state', 'remark')
    list_per_page = 10
    ordering = ['-id']
    autocomplete_fields = ('product_order_id',)
    # list_editable = ('reservation_date','start_date','end_date')
    # actions_selection_counter = False

    def user_name(self,obj):
        return '{0}({1})'.format(obj.product_order_id.user_id.name,obj.product_order_id.user_id.telephone)
    user_name.short_description = u"??????"

    def unit_price(self,obj):
        return obj.product_order_id.unit_price
    unit_price.short_description = u"??????"


    def delete_selected(self, request, queryset):
        count = 0
        if queryset.filter(state=2).count()>0:
            msg = '???????????????????????????????????????????????????????????????'
            self.message_user(request, msg,level=messages.ERROR)
        else:
            for i in queryset:
                if i.state == 1:
                    i.delete()
                    count += 1
            if count > 0:
                msg = '???????????????{}???????????????'.format(count)
            else:
                msg = '?????????????????????'
            self.message_user(request, msg, level=messages.SUCCESS if count>0 else messages.WARNING)
    delete_selected.short_description = '???????????????'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.state==2:
            return ["product_order_id", "teacher_id",'state']
        else:
            return ['state']

    # ??????
    def commit_check(self,request,queryset):
        count = 0
        if queryset.filter(state__in=[2, 3]).count()>0:
            msg = '??????????????????????????????????????????????????????????????????'
            self.message_user(request, msg, level=messages.ERROR)
        else:
            for i in queryset:
                if i.state == 1:
                    obj = VipProductOrder.objects.get(id=i.product_order_id.id)
                    if obj.remain_count > 0:
                        obj.remain_count -= 1
                        obj.save()
                        i.state = 2
                        i.save()
                        msg = '????????????'
                        self.message_user(request, msg, level=messages.SUCCESS)
                    else:
                        msg = '{}:?????????????????????????????????'.format(i.product_order_id)
                        self.message_user(request, msg, level=messages.ERROR)

    commit_check.confirm = '???????????????'
    commit_check.short_description = u"????????????"
    commit_check.icon = 'fas fa-check'

    # ??????element-ui????????????????????????https://element.eleme.cn/#/zh-CN/component/button
    commit_check.type = 'success'

    # ?????????????????????????????????
    # commit_check.style = 'color:black;'

    #????????????
    def commit_cancel(self,request,queryset):
        count = 0
        if queryset.filter(state__in=[2, 3]).count()>0:
            msg = '?????????????????????????????????????????????????????????'
            self.message_user(request, msg, level=messages.ERROR)
        else:
            for i in queryset:
                if i.state == 1:
                    i.state = 3
                    count += 1
                    i.save()
            if count > 0:
                msg = '???????????????{}???????????????'.format(count)
            else:
                msg = '???????????????????????????'
            self.message_user(request, msg, level=messages.SUCCESS if count>0 else messages.WARNING)

    commit_cancel.confirm = '?????????????????????'
    commit_cancel.short_description = u"????????????????????????"
    commit_cancel.type = 'warning'


admin.AdminSite.site_header = '??????????????????'
admin.AdminSite.site_title = '??????????????????'

admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(VipProduct, VipProductAdmin)
admin.site.register(VipProductOrder, VipProductOrderAdmin)
admin.site.register(CourseRecord, CourseRecordAdmin)


admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)


