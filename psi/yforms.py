# -*- coding: UTF-8 -*-
from datetime import datetime
from django import forms
from psi.models import Shop,SellOrder,Remit,Staff,Category
from django.contrib.auth.models import User
from django.forms import ModelForm
import re
'''
def get_shop(request):
    if len(request)>0:
        shop = request.user.get_profile().shop
        if shop>0:
            return shop
        else:
            return 0
'''


class YLogin(forms.Form):
    username = forms.CharField(max_length=20,label='姓名')
    password = forms.CharField(max_length=10,widget=forms.PasswordInput(),label='密码')


class CustomerAdd(forms.Form):
    name = forms.CharField(max_length=10,min_length=2,label='姓名 * ',error_messages={'required': '必填项','min_length':'用户名需2位字符以上','man_length':'用户名不得长于10位'})
    code = forms.CharField(max_length=20,min_length=4,label='会员卡号',error_messages={'min_length':'会员编号需4位字符以上','man_length':'会员编号不得长于20位'},required=False)
    #shop = forms.ModelChoiceField(queryset=Shop.objects.exclude(name='总部'),label='店铺 * ',empty_label='请选择所注册商店',widget = forms.Select()) #queryset=Shop.objects.filter(hidden=False)
    telephone = forms.CharField(max_length=11,label='手机/电话号码',required=False)
    address = forms.CharField(max_length=100,label='地址',required=False)
    joindate = forms.DateField(initial=datetime.now(),label='注册日期 * ',error_messages={'invalid':'日期格式:2012-05-30'})
    note = forms.CharField(max_length=100,label='备注',required=False,widget=forms.Textarea(attrs={'rows':'5'}))
    def clean(self):
        cleaned_data = self.cleaned_data
        cName = cleaned_data.get("name")
        cCode = cleaned_data.get("code")
        cTelephone = cleaned_data.get("telephone")
        Reg = re.match(ur"^[\u4e00-\u9fa5]{2,}$",cName)
        if Reg is None:
            self._errors["name"] = self.error_class([u"会员名不能少于2位中文字符"])
        if cCode:
            Reg = re.match(ur"^[A-Za-z0-9]{4,20}$",cCode)
            if Reg is None:
                self._errors["code"] = self.error_class([u"编号由4位以上数字及字母组成"])
        if cTelephone:
            Reg = re.match(ur"^([1-9]\d{6,7})|([1-9]\d{10})$",cTelephone)
            if Reg is None:
                self._errors["telephone"] = self.error_class([u"只可为电话或手机号码"])
        return cleaned_data

sp_choices =((1, '罗莱'),(2, '优家'),(3,'宝缦'),(4,'其他'))
class RemitAdd(forms.Form):
    supplier = forms.ChoiceField(label="收款单位 * ",choices=sp_choices)
    staff = forms.ModelChoiceField(label="办理人员 * ",queryset=Staff.objects.filter(level__lt=99))
    amount = forms.DecimalField(label="汇款金额 * ",max_digits=8,decimal_places=2,localize=True)
    date = forms.DateField(label="汇款日期 * ")
    hidden = forms.BooleanField(label="删除标记 * ",widget=forms.CheckboxInput,required=False)
    note = forms.CharField(label="备注 ",required=False,max_length=100,widget=forms.Textarea(attrs={'rows':'5'}))

class InStream(forms.Form):
    code = forms.CharField(label="单号",required=False)
    supplier = forms.ChoiceField(label="供货单位 * ",choices=sp_choices)
    date = forms.DateField(label="日期 * ")
    keeper = forms.ModelChoiceField(label="仓管 * ",queryset=Staff.objects.filter(level__lt=5),widget=forms.Select)
    staff1 = forms.ModelChoiceField(label="经办 * ",queryset=Staff.objects.filter(level__gte=5),widget=forms.Select)
    hidden = forms.BooleanField(label="删除标记",widget=forms.CheckboxInput,required=False)
    note = forms.CharField(max_length=100,label="备注",widget=forms.Textarea(attrs={'rows':'5'}),required=False)
    def clean(self):
        cleaned_data = self.cleaned_data
        cCode = cleaned_data.get("code")
        if cCode:
            Reg = re.match(ur"^[A-Za-z0-9]{4,20}$",cCode)
            if Reg is None:
                self._errors["code"] = self.error_class([u"编号由4位以上数字及字母组成。"])
        return cleaned_data

class OutStream(InStream):
    from psi.models import InStream
    supplier = forms.ModelChoiceField(label="取货店铺 * ",queryset=Shop.objects.exclude(name=u"总部"),initial=1,widget=forms.Select)
    instream = forms.ModelChoiceField(label="入库单绑定 ",empty_label="不予绑定",required=False,queryset=InStream.objects.filter(hidden=0),widget=forms.Select,help_text="非可逆操作，请谨慎选择")

class Product(forms.Form):
    name = forms.CharField(label="名称 *",min_length=2,max_length=30)
    barcode = forms.CharField(label="条形码",max_length=20,required=False)
    size = forms.CharField(label="尺寸",max_length=20,required=False)
    category = forms.ModelChoiceField(label="类别 *",queryset=Category.objects.filter(hidden=0,pid__in=Category.objects.filter(hidden=0,pid__isnull=False).distinct("pid").values_list("pid")) ,widget=forms.Select)
    hidden = forms.BooleanField(label="删除标记",widget=forms.CheckboxInput,required=False)
    note = forms.CharField(max_length=100,label="备注",widget=forms.Textarea(attrs={"rows":"5"}),required=False)

class PWd(forms.Form):
    sid = forms.CharField()
    opwd = forms.CharField(label="原有密码 *",max_length=10,widget=forms.PasswordInput)
    pwd = forms.CharField(label="新设密码 *",min_length=4,max_length=10,widget=forms.PasswordInput)
    pwd2 = forms.CharField(label="密码确认 *",min_length=4,max_length=10,widget=forms.PasswordInput)
    

class OrderAdd(ModelForm):
    class Meta:
        model = SellOrder