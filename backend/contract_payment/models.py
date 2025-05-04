from django.db import models
from django.conf import settings

class Contract(models.Model):
    """合同信息"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待签署'),
        ('signed', '已签署'),
        ('completed', '已完成'),
        ('terminated', '已终止'),
    )
    
    title = models.CharField(max_length=200, verbose_name="合同标题")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_contracts", verbose_name="客户")
    consultant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultant_contracts", verbose_name="顾问")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    content = models.TextField(verbose_name="合同内容")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="合同总金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    attachment = models.FileField(upload_to='contracts/', blank=True, null=True, verbose_name="附件")
    
    class Meta:
        verbose_name = "合同"
        verbose_name_plural = "合同"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

class Payment(models.Model):
    """支付信息"""
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('refunded', '已退款'),
        ('failed', '支付失败'),
    )
    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="payments", verbose_name="关联合同")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="支付金额")
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="支付日期")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="支付方式")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="交易ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "支付记录"
        verbose_name_plural = "支付记录"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.contract.title} - {self.amount}"

class Invoice(models.Model):
    """发票信息"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('issued', '已开具'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
    )
    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="invoices", verbose_name="关联合同")
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="发票号码")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="发票金额")
    issue_date = models.DateField(verbose_name="开具日期")
    due_date = models.DateField(verbose_name="到期日期")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "发票"
        verbose_name_plural = "发票"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Invoice #{self.invoice_number}"
