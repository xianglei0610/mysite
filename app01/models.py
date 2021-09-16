from django.db import models

from django.utils.html import format_html

from django.shortcuts import render, reverse, redirect

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('学员姓名', max_length=30)
    telephone = models.CharField('学员电话', max_length=100, unique=True, null=False)
    gender = models.CharField('性别', max_length=3, choices=[('F',"女"), ('M',"男")], default='M')
    age = models.IntegerField('年龄')
    id_card = models.CharField('学员身份证', max_length=30)
    remark = models.TextField(u'备注',  editable=True, null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)

    def __str__(self):
        return "{0}({1})".format(self.name, self.telephone)

    class Meta:
        verbose_name = "学员管理"    # 表名改成中文名
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('老师姓名', max_length=30)
    telephone = models.CharField('老师电话', max_length=100, unique=True, null=False)
    gender = models.CharField('性别', max_length=3, choices=[('F',"女"), ('M',"男")], default='M')
    status = models.CharField('状态',
        max_length=2,
        choices=[('Y',"在职"), ('N',"离职")],
        default='Y',
    )
    remark = models.TextField(u'备注',  editable=True, null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)

    def __str__(self):
        return "{0}({1})".format(self.name, self.telephone)

    class Meta:
        verbose_name = "老师管理"    # 表名改成中文名
        verbose_name_plural = verbose_name


class VipProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('会员卡名称', max_length=64, unique=True)
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    count = models.IntegerField('次数')
    remark = models.TextField(u'备注',  editable=True, null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "会员卡课程管理"
        verbose_name_plural = verbose_name


class CourseRecord(models.Model):
    id = models.AutoField(primary_key=True)
    product_order_id = models.ForeignKey('VipProductOrder', on_delete=models.CASCADE, verbose_name="课程名称",related_name='courses')
    teacher_id = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name="老师")

    reservation_date = models.DateTimeField(u'预约时间', default=None, null=True, blank=True)
    start_date = models.DateTimeField(u'课程开始时间', default=None, null=True, blank=True)
    end_date = models.DateTimeField(u'课程结束时间', default=None, null=True, blank=True)
    remark = models.TextField(u'备注',  editable=True, null=True, blank=True)
    state = models.IntegerField(verbose_name = u"状态", choices = ((1, u'已预约'), (2, u'已签到'), (3, u'已取消')), default = 1)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)

    def __str__(self):
        return "{0}_{1}".format(str(self.id), self.product_order_id)


    class Meta:
        verbose_name = "上课记录"    # 表名改成中文名
        verbose_name_plural = verbose_name


    def print_record(self):
        if self.state== 2:
            parameter_str = 'record_id={}'.format(str(self.id))
            color_code = ''
            btn_str = '<a target="_blank" class="btn btn-xs btn-danger" href="{}"> <input name="打印"  type="button" id="passButton"  class="btn btn-xs btn-danger"  title="打印上课记录" value="打印"> </a>'
            return format_html(btn_str, '/print_record/?{}'.format(parameter_str))
        else:
            return '--'
    print_record.action_type = 1
    print_record.short_description = '操作'


class VipProductOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="学员")
    product_id = models.ForeignKey('VipProduct', on_delete=models.CASCADE, verbose_name="课程名称")
    price = models.DecimalField('购买消费金额', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('单次课程金额', max_digits=10, decimal_places=2)
    count = models.IntegerField('购买课程次数')
    remain_count = models.IntegerField('剩余次数', default=0, editable=True)
    start_date = models.DateField(u'有效期开始日期', default=None, null=True, blank=True)
    deadline_date = models.DateField(u'有效期截止日期', default=None, null=True, blank=True)
    state = models.IntegerField(verbose_name= u"状态", choices = ((1, u'已创建'), (2, u'已付款'), (3, u'已取消')), default = 1)
    remark = models.TextField(u'备注',  editable=True, null=True, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)

    def __str__(self):
        return "{0}_{1}({2})_{3}".format(str(self.id), self.user_id.name, self.user_id.telephone, self.product_id.name)

    def save(self, *args, **kwargs):
        self.unit_price = self.price / self.count
        super(VipProductOrder, self).save(*args, **kwargs) # Call the "real" save() method.

    def use_count(self):
        use_count = 0
        # print(self.courses.all(),self.id,self.state)
        if self.state == 2:
            use_count = self.courses.filter(product_order_id=self.id, state=2).count()
            url = reverse('admin:app01_courserecord_changelist') +'?product_order_id=%s&state=2'%self.id
            return format_html("<a target='_top' class='related-widget-wrapper-link' href=%s> %s </a>"%(url, use_count))
        else:
            return use_count
    use_count.short_description = '上课次数'


    class Meta:
        verbose_name = "购买课程记录"
        verbose_name_plural = verbose_name