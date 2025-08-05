from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class PaymentMethod(models.Model):
    """
    Available payment methods
    """
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_online = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    processing_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    fixed_fee = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    min_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    max_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)]
    )
    icon = models.ImageField(upload_to='payment_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Currency(models.Model):
    """
    Supported currencies
    """
    code = models.CharField(max_length=3, unique=True)  # USD, EUR, etc.
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6, default=1.000000)
    is_base_currency = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Transaction(models.Model):
    """
    All financial transactions
    """
    TRANSACTION_TYPES = (
        ('ad_payment', 'Advertisement Payment'),
        ('subscription', 'Subscription Payment'),
        ('commission', 'Commission Payment'),
        ('refund', 'Refund'),
        ('deposit', 'Security Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('penalty', 'Penalty Fee'),
        ('bonus', 'Bonus Credit'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    )

    # Basic Information
    transaction_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount Information
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6, default=1.000000)
    amount_usd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Fees
    processing_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Payment Details
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(blank=True, null=True)
    
    # Related Objects
    advertisement = models.ForeignKey(
        'ad.Advertisement', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='payments'
    )
    tariff_plan = models.ForeignKey(
        'tariffplans.TariffPlan', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='payments'
    )
    
    # Additional Information
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    receipt_url = models.URLField(blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    # Refund Information
    refunded_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    refund_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.user.email} - {self.amount} {self.currency.code}"

    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.amount + self.processing_fee + self.platform_fee
        
        # Convert to USD for reporting
        if self.currency.code != 'USD':
            self.amount_usd = self.amount * self.exchange_rate
        else:
            self.amount_usd = self.amount
            
        super().save(*args, **kwargs)


class PaymentAccount(models.Model):
    """
    User payment accounts for receiving money
    """
    ACCOUNT_TYPES = (
        ('bank_account', 'Bank Account'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('wallet', 'Digital Wallet'),
        ('crypto', 'Cryptocurrency'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_accounts')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)
    routing_number = models.CharField(max_length=50, blank=True)
    swift_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', 'account_name']

    def __str__(self):
        return f"{self.user.email} - {self.account_name}"

    def save(self, *args, **kwargs):
        # Ensure only one primary account per user
        if self.is_primary:
            PaymentAccount.objects.filter(
                user=self.user, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """
    Invoices for services
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='invoice', 
        blank=True, 
        null=True
    )
    
    # Invoice Details
    subject = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    
    # Dates
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateTimeField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    
    # Files
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        self.total_amount = self.amount + self.tax_amount - self.discount_amount
        super().save(*args, **kwargs)


class Refund(models.Model):
    """
    Refund requests and processing
    """
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )

    REFUND_TYPES = (
        ('full', 'Full Refund'),
        ('partial', 'Partial Refund'),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='refunds')
    refund_type = models.CharField(max_length=10, choices=REFUND_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='requested')
    
    # Processing
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_refunds'
    )
    processing_notes = models.TextField(blank=True)
    gateway_refund_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"Refund {self.transaction.transaction_id} - {self.amount}"


class WalletBalance(models.Model):
    """
    User wallet balances for different currencies
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet_balances')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    locked_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'currency']
        ordering = ['currency__code']

    def __str__(self):
        return f"{self.user.email} - {self.balance} {self.currency.code}"

    @property
    def available_balance(self):
        return self.balance - self.locked_balance
