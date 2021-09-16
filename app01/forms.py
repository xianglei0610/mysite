#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: xiang
# @Date  : 2021/3/2
# @Desc  :

from .models import  User, Teacher, CourseRecord, VipProduct,VipProductOrder
from django import forms
import re


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'telephone', 'gender', 'age','id_card', 'remark']

    def clean_telephone(self):  # 函数必须以clean_开头
        """
        通过正则表达式验证手机号码是否合法
        """
        mobile = self.cleaned_data['telephone']
        mobile_regex = r'^1[3456789]\d{9}$'
        p = re.compile(mobile_regex)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'telephone', 'gender', 'status', 'remark']

    def clean_telephone(self):  # 函数必须以clean_开头
        """
        通过正则表达式验证手机号码是否合法
        """
        mobile = self.cleaned_data['telephone']
        mobile_regex = r'^1[3456789]\d{9}$'
        p = re.compile(mobile_regex)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')


class VipProductForm(forms.ModelForm):

    class Meta:
        model = VipProduct
        fields = ['name', 'amount', 'count', 'remark']

    def clean(self):
        amount = self.cleaned_data.get('amount',0)
        count = self.cleaned_data.get('count',0)
        if amount>0 and count>0:
            pass
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError('金额或者次数必须大于0')
        return self.cleaned_data

class VipProductOrderForm(forms.ModelForm):

    class Meta:
        model = VipProductOrder
        fields = ('user_id', 'product_id', 'price', 'count', 'start_date','deadline_date','remain_count','state', 'remark')

    def clean(self):
        price = self.cleaned_data.get('price',0)
        count = self.cleaned_data.get('count',0)
        if price>0 and count>0:
            pass
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError('金额或者次数必须大于0')
        return self.cleaned_data


