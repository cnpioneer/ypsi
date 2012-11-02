# -*- coding: UTF-8 -*-

from datetime import datetime
import decimal
from django.db.models import Sum
from django.db import models,connection
from django.contrib.auth.models import User


sp_choices =((1, '罗莱'),(2, '优家'),(3,'宝缦'),(4,'其他'))#(99,'退库')

class Posts(models.Model):
    title = models.CharField(max_length=20,help_text="标题")
    note = models.CharField(max_length=100,help_text="公告内容")
    date = models.DateField(auto_now_add=True,help_text="发布日期")
    hidden = models.BooleanField(default=False,help_text="删除标记")
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name_plural = ('公告管理')


class Shop(models.Model):
    name = models.CharField(max_length=20,help_text="店铺名称")
    telephone = models.CharField(max_length=11,help_text="电话")
    address = models.CharField(max_length=100,help_text="地址")
    opendate = models.DateField(help_text="开业日期",default=datetime.now())
    #hidden = models.BooleanField(default=False,help_text="是否隐藏") 更新时增加
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = ('店铺管理')


class Staff(models.Model):
    user = models.ForeignKey(User,unique=True,max_length=10,help_text="绑定ID")
    name = models.CharField(max_length=10,help_text="姓名")
    sex = models.CharField(max_length=2,help_text="性别",choices=(('F', '女性'),('M', '男性')),default='F')
    image = models.ImageField(upload_to='staffs',blank=True,null=True,help_text="照片")
    edu = models.CharField(max_length=4,help_text="学历")
    marital = models.BooleanField(help_text="婚否",choices=((True, '已婚'),(False, '未婚')))
    school = models.CharField(max_length=100,help_text="毕业学校",blank=True,null=True)
    graduation = models.DateField(help_text="毕业日期",blank=True,null=True)
    address = models.CharField(help_text="住址",max_length=100)
    cellphone = models.CharField(help_text="手机",max_length=11)
    idcode = models.CharField(help_text="身份证号",max_length=18,unique=True)
    homephone = models.CharField(help_text="紧急联系电话",max_length=11)
    shop = models.ForeignKey(Shop,help_text="店铺")
    level = models.SmallIntegerField(max_length=2,help_text="岗位",choices=((1, '董事'),(2,'会计'),(3,'仓管'),(4,'经理'),(5,'店长'),(6,'店员'),(7,'后勤'),(8,'实习'),(9,'其他'),(99,'离职')),default=6)
    joindate = models.DateField(default=datetime.now(),help_text="入职日期")
    exwork = models.CharField(help_text="工作经历",max_length=255,blank=True,null=True)
    family = models.CharField(help_text="家庭成员及关系",max_length=255)
    note = models.CharField(help_text="备注",max_length=100,blank=True,null=True)
    def get_level_display(self):
        pass
    def __unicode__(self):
        return (u"%s %s") %(self.get_level_display(),self.name)#显示Choices的值
    class Meta:
        verbose_name_plural = ('人员管理')


class PaySlip(models.Model):
    staff = models.ForeignKey(Staff,help_text="员工")
    pay = models.DecimalField(max_digits=7,decimal_places=2,help_text="工资")
    date = models.DateField(default=datetime.now(),help_text="发薪日期")
    note = models.CharField(help_text="备注",max_length=100,blank=True)
    def __unicode__(self):
        return u"%s %s 薪资 %s" %(self.date,self.staff,self.pay)
    class Meta:
        verbose_name_plural = ('薪资发放记录')

class Customer(models.Model):
    name = models.CharField(max_length=10,help_text="顾客姓名")
    code = models.CharField(max_length=20,help_text="编号",blank=True,null=True)
    shop = models.ForeignKey(Shop,help_text="店铺")
    telephone = models.CharField(max_length=11,help_text="联系电话",blank=True,null=True)
    address = models.CharField(max_length=100,help_text="地址",blank=True,null=True)
    joindate = models.DateField(default=datetime.now(),blank=True,null=True,help_text="加入日期")
    hidden = models.BooleanField(default=False,help_text="删除标记")
    note = models.CharField(help_text="备注",max_length=100,blank=True,null=True)
    def get_total_amount(self): #自定义属性
        if len(SellOrder.objects.filter(customer = self))>0:
            cursor = connection.cursor()
            cursor.execute("select sum(quantity*price)-(ifnull(discount,0)) as total from psi_sellorderdetail,psi_sellorder where psi_sellorder.hidden=0 and psi_sellorder.id=psi_sellorderdetail.oid_id and psi_sellorder.customer_id=%s group by psi_sellorder.customer_id order by psi_sellorder.id desc",[self.id])
            total =cursor.fetchone()[0]
            cursor.close()
            return total
    amount = property(get_total_amount)

    def __unicode__(self):
        return ("%s|%s|%s|%d") %(self.name,self.code,self.telephone,self.id)
    class Meta:
        verbose_name_plural = ('顾客管理')

class Category(models.Model):
    name = models.CharField(max_length=10,help_text="分类名称")
    pid = models.ForeignKey('self', blank=True, null=True,help_text="父级分类")
    hidden = models.BooleanField(default=False,help_text="是否隐藏")
    def __unicode__(self):
        if self.pid is not None:
            return ("%s-%s") %(self.pid.name,self.name)
        else:
            return ("%s") %self.name

    class Meta:
        verbose_name_plural = ('分类管理')

class Products(models.Model):
    name = models.CharField(max_length=30,help_text="商品名称")
    barcode = models.CharField(max_length=20,blank=True,null=True,help_text="条形码")
    image = models.ImageField(upload_to='products',blank=True,null=True,help_text="商品图片")
    category = models.ForeignKey(Category,help_text="类别")
    size = models.CommaSeparatedIntegerField(max_length=20,help_text="尺寸,请使用','号分割,如230,180",blank=True,null=True)
    hidden = models.BooleanField(default=False,help_text="删除标记")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def _get_full_name(self):
        return ("%s|%s|%d") %(self.name,self.barcode,self.id)
    full_name = property(_get_full_name)
    def _get_avg_value(self):#获取出库商品平均值
        tamount_and_tquantity = InDetail.objects.filter(product=self.id,inid__in=InStream.objects.filter(hidden=0)).extra(select={'t_in_amount':'sum(value*quantity)','t_in_quantity':'sum(quantity)','value':'value'}).order_by("-id")[0]
        t_in_amount = tamount_and_tquantity.t_in_amount
        t_in_quantity = tamount_and_tquantity.t_in_quantity
        t_value = tamount_and_tquantity.value
        t_out_quantity = OutDetail.objects.filter(product=self.id,outid__in=OutStream.objects.filter(hidden=0)).aggregate(Sum('quantity'))['quantity__sum']
        t_in_quantity = 0 if t_in_quantity is None else t_in_quantity
        t_out_quantity = 0 if t_out_quantity is None else t_out_quantity
        if  t_in_quantity is 0 or t_in_amount is None or t_in_amount is 0:
            avg = 0
        else:
            decimal.getcontext().prec = 12
            avg =  decimal.Decimal(str(float(t_in_amount)/float(t_in_quantity))).quantize(decimal.Decimal('0.01'))#取小数点后两位精度
        return avg,t_in_quantity-t_out_quantity,t_value,t_in_quantity,t_out_quantity
    p_str = property(_get_avg_value)

    def __unicode__(self):
        return u"%s 当前均价 %s 剩余库存 %s" %(self.name,self.p_str[0],self.p_str[1])
    class Meta:
        verbose_name_plural = ('商品管理')

class Depot(models.Model):
    name = models.CharField(max_length=10,help_text="仓库名")
    address = models.CharField(max_length=100,help_text="仓库地址")
    hidden = models.BooleanField(default=False,help_text="是否隐藏")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def get_total_amount(self): #自定义属性
        if len(InDetail.objects.filter(depot = self))>0:
            cursor = connection.cursor()
            cursor.execute("select ifnull(sum(tquantity),0),ifnull(sum(tquantity*avgvalue),0) from"
                           "(select did,tquantity,sum(value*quantity)/sum(quantity) as avgvalue from psi_indetail,psi_instream join"
                           "(select depot_id as did, psi_indetail.product_id as pid2,sum(psi_indetail.quantity)-ifnull(toq,0) as tquantity from psi_indetail left join"
                           "(select psi_outdetail.product_id as pid, sum(psi_outdetail.quantity) as toq from psi_outdetail,psi_outstream  where depot_id=%s and psi_outstream.id=psi_outdetail.outid_id and psi_outstream.hidden=0  group by pid) on pid2=pid where depot_id=%s group by pid2)"
                           "on psi_indetail.product_id=pid2 where psi_instream.id=psi_indetail.inid_id and psi_instream.hidden=0 group by psi_indetail.product_id ) group by did;",[self.id,self.id])
            t_quantity_and_amount =cursor.fetchone()
            cursor.close()
        else:
            t_quantity_and_amount=(0,0)
        return t_quantity_and_amount
    d_str = property(get_total_amount)
    def __unicode__(self):
        return u"%s 当前货物 %s 件 总价值 [%s] 元" %(self.name,self.d_str[0],self.d_str[1])
    class Meta:
        verbose_name_plural = ('仓库管理')

class InStream(models.Model): #出入库分离
    code = models.CharField(max_length=30,unique=True,help_text="入库单号")
    supplier = models.SmallIntegerField(max_length=2,choices=sp_choices,help_text="供应商")
    date = models.DateField(help_text="日期",default=datetime.now())#改为Date
    keeper = models.ForeignKey(Staff,related_name='in_keeper_set',help_text="仓管")
    staff1 = models.ForeignKey(Staff,related_name='in_sells_1_set',help_text="收货人一")
    staff2 = models.ForeignKey(Staff,related_name='in_sells_2_set',blank=True,null=True,help_text="收货人二")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    hidden = models.BooleanField(default=False,help_text="删除标记")
    def get_total_amount(self):#自定义属性
        if len(InDetail.objects.filter(inid=1))>0:
            t_quantity_and_amount= (InDetail.objects.filter(inid=self.id).extra(select={'t_count':'count(id)','t_quantity':'sum(quantity)','t_amount':'sum(quantity*value)'}))[0]
            return t_quantity_and_amount.t_count,t_quantity_and_amount.t_quantity,t_quantity_and_amount.t_amount
        else:
            return 0,0
    i_str = property(get_total_amount)
    def __unicode__(self):
        return u"%s 经 %s、%s 办理 共%s种%s件 价值%s元 [%s]" %(self.code,self.keeper,self.staff1,self.i_str[0],self.i_str[1],self.i_str[2],self.date)
    class Meta:
        verbose_name_plural = ('入库管理')

class InDetail(models.Model):
    inid = models.ForeignKey(InStream,help_text="入库单ID")
    product = models.ForeignKey(Products,help_text="商品")
    value = models.DecimalField(max_digits=8,decimal_places=2,help_text="厂方进价")
    quantity = models.IntegerField(max_length=5,help_text="数量")
    depot = models.ForeignKey(Depot,help_text="出入库库房")
    depotdetail = models.CharField(max_length=100,blank=True,null=True,help_text="出入库详细位置")
    def _get_amount(self): #自定义属性金额小计
        return self.quantity*self.value
    amount = property(_get_amount)
    def __unicode__(self):
        return (u"%d:%s %d 套，小计 %s 元") %(self.inid_id,self.product.name,self.quantity,self.amount)#此处使用了%s而非%d提高Decimal类型数据精度
    class Meta:
        verbose_name_plural = ('入库详单')

class OutStream(models.Model):
    code = models.CharField(max_length=30,unique=True,help_text="出库单据号")
    date = models.DateTimeField(help_text="日期",default=datetime.now())
    keeper = models.ForeignKey(Staff,related_name='out_keeper_set',help_text="仓管")
    staff1 = models.ForeignKey(Staff,related_name='out_sells_1_set',help_text="提货人一")
    staff2 = models.ForeignKey(Staff,related_name='out_sells_2_set',blank=True,null=True,help_text="提货人二")
    shop = models.ForeignKey(Shop,help_text="提货店铺")
    hidden = models.BooleanField(default=False,help_text="删除标记")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def get_total_amount(self): #自定义属性
        if len(OutDetail.objects.filter(outid = self.id))>0:
            cursor = connection.cursor()
            cursor.execute("select sum(quantity),sum(quantity*avgvalue) as ta from psi_outdetail  join"
                           "(select psi_indetail.product_id as pid,sum(value*quantity)/sum(quantity) as avgvalue from psi_indetail  group by product_id having product_id in "
                           "(select psi_outdetail.product_id from psi_outdetail where psi_outdetail.outid_id=%s))on psi_outdetail.outid_id=%s and product_id=pid;",[self.id,self.id])
            t_quantity_and_amount =cursor.fetchone()
            cursor.close()
            return t_quantity_and_amount[0],round(t_quantity_and_amount[1],2)
        else:
            return 0,0

    total = property(get_total_amount)

    def __unicode__(self):
        return u"%d:%s 经 [%s] 办理,共 %s 件, 价值[%s] 元" %(self.id,self.date,self.keeper,self.total[0],self.total[1])
    class Meta:
        verbose_name_plural = ('出库管理')

class OutDetail(models.Model):
    outid = models.ForeignKey(OutStream,help_text="出库单ID")
    product = models.ForeignKey(Products,help_text="商品")
    quantity = models.IntegerField(max_length=5,help_text="数量")
    depot = models.ForeignKey(Depot,help_text="出入库库房")
    def _get_amount(self): #自定义属性金额小计
        return self.quantity*self.product.p_str[0]
    amount = property(_get_amount)
    def __unicode__(self):
        return u"%d： %s %d 套，小计 %s 元" %(self.outid_id,self.product.name,self.quantity,self.amount)#此处使用了%s而非%d提高Decimal类型数据精度
    class Meta:
        verbose_name_plural = ('出库详单')


class SellOrder(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,help_text="销售单据号")#销售单据号
    customer = models.ForeignKey(Customer,blank=True,null=True,help_text="顾客")
    shop = models.ForeignKey(Shop,help_text="店铺")
    staff = models.ForeignKey(Staff,help_text="销售员工")
    #discount = models.IntegerField(max_length=6,default=0,blank=True,null=True,help_text="折扣金额")
    discount = models.DecimalField(max_digits=8,decimal_places=2,default=0,blank=True,null=True,help_text="折扣金额")
    date = models.DateTimeField(help_text="日期")
    hidden = models.BooleanField(default=False,help_text="删除标记")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def _total_amount(self): #自定义属性
        if len(SellOrderDetail.objects.filter(oid = self))>0:
            cursor = connection.cursor()
            cursor.execute("select sum(quantity*price) as total from psi_SELLORDERDETAIL where oid_id=%s group by oid_id",[self.id])
            if self.discount is not None:

                total =float(cursor.fetchone()[0])-float(self.discount)
            else:
                total =cursor.fetchone()[0]
            cursor.close()
        else:
            total=0
        return total
    total = property(_total_amount)
    def __unicode__(self):
        return u"%s %s 售%s元 [%s]" %(self.shop,self.staff.name,self.total,self.date)
    class Meta:
        verbose_name_plural = ('销售管理')


class SellOrderDetail(models.Model):
    oid = models.ForeignKey(SellOrder,help_text="销售单据号")
    product = models.ForeignKey(Products,help_text="商品")
    quantity = models.IntegerField(max_length=4,help_text="数量")
    price = models.DecimalField(max_digits=8,decimal_places=2,help_text="价格")
    def _get_amount(self): #小计金额
        return self.quantity*self.price
    amount = property(_get_amount)
    def __unicode__(self):
        return u'订单%d: %d 件 %s，共 %s 元' %(self.oid.id,self.quantity,self.product.name,self.amount)
    class Meta:
        verbose_name_plural = ('销售详单')


class Remit(models.Model):#增加汇款记录管理
    supplier = models.SmallIntegerField(max_length=2,choices=sp_choices,help_text="供应商")
    amount = models.DecimalField(max_digits=8,decimal_places=2,help_text="金额")
    staff = models.ForeignKey(Staff,help_text="汇款人")
    date = models.DateField(default=datetime.now(),help_text="汇款日期") #修改为日期
    hidden = models.BooleanField(default=False,help_text="删除标记")
    note = models.CharField(max_length=100,blank=True,null=True,help_text="备注")
    def __unicode__(self):
        return u"%s %s 汇出 %s 元" %(self.date,self.staff,self.amount)
    class Meta:
        verbose_name_plural = ('汇款记录')
