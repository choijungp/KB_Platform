from django.db import models
from platformdirs import user_log_dir
from django.contrib.auth.models import User

# Create your models here.
# 계좌 DB
class Account(models.Model):
    acc_choices = [
        (0, '은행'),
        (1, '증권'),
        (2, '금'),
    ]

    acc_detail = [
        (0, '입출금자유'),
        (1, '예금/적금/주택청약'),
        (2, '골드'),
        (3, '증권'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account")
    acc_num = models.CharField(max_length=30, primary_key=True)  # 계좌번호 PK
    acc_pwd = models.PositiveIntegerField()           # 계좌 비밀번호 (6자리)
    acc_type = models.CharField(max_length=50, choices=acc_choices)     # 계좌 타입 (은행, 증권, 금)
    acc_name = models.CharField(max_length=20)        # 계좌명
    total = models.IntegerField(null=True, blank=True)                     # 총 잔액
    created_at = models.DateField()  # 계좌 개설일자
    updated_at = models.DateField(auto_now=True)      # 최근 거래일자
    acc_detail = models.CharField(max_length=50, choices=acc_detail)   # 계좌 디테일
    
    def __str__(self):
        return self.acc_name

# 거래 내역 DB
class Trans(models.Model):
    trans_choices = [
        (0, '식비'),
        (1, '이동통신'),
        (2, '쇼핑'),
        (3, '문화생활'),
        (4, '의료'),
        (5, '교통비'),
    ]
    # trans_id :: PK 자동 생성
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='trans')
    trans_date = models.DateTimeField()    # 거래 시간
    trans_price = models.IntegerField()                 # 거래 금액
    trans_content = models.CharField(max_length=30)     # 거래 내용 
    trans_type = models.CharField(max_length=50, choices=trans_choices)   


# Card DB
class Card(models.Model):
    # card_id :: 카드 아이디
    card_name = models.CharField(max_length=20)
    card_type = models.BooleanField() # true : 신용카드, false : 체크카드
    card_img = models.ImageField(blank=True, upload_to ="media", null=True)

# Benefit DB
class Benefit(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default='')
    service_name = models.CharField(max_length=20)
    percent = models.IntegerField()
    use_stand = models.TextField()
    month_stand = models.TextField()
    
    class Meta:
        db_table = "kb_platform_benefit"

# lstm model result
class LSTM(models.Model):
    date = models.DateField()
    pred = models.IntegerField() 
    act = models.IntegerField()