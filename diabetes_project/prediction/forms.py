from django import forms

class DiabetesForm(forms.Form):
    GENDER_CHOICES = [('Female', 'Nữ'), ('Male', 'Nam'), ('Other', 'Khác')]
    SMOKING_CHOICES = [
        ('never', 'Chưa từng hút'),
        ('No Info', 'Không có thông tin'),
        ('current', 'Đang hút'),
        ('former', 'Đã từng hút'),
        ('not current', 'Hiện tại không hút'),
        ('ever', 'Đã từng (Ever)')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Giới tính", widget=forms.Select(attrs={'class': 'form-select'}))
    age = forms.FloatField(label="Tuổi", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'VD: 45'}))
    hypertension = forms.ChoiceField(choices=[(0, 'Không'), (1, 'Có')], label="Cao huyết áp", widget=forms.Select(attrs={'class': 'form-select'}))
    heart_disease = forms.ChoiceField(choices=[(0, 'Không'), (1, 'Có')], label="Bệnh tim mạch", widget=forms.Select(attrs={'class': 'form-select'}))
    smoking_history = forms.ChoiceField(choices=SMOKING_CHOICES, label="Lịch sử hút thuốc", widget=forms.Select(attrs={'class': 'form-select'}))
    bmi = forms.FloatField(label="Chỉ số BMI", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'VD: 25.5'}))
    HbA1c_level = forms.FloatField(label="Chỉ số HbA1c", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'VD: 6.5'}))
    blood_glucose_level = forms.FloatField(label="Đường huyết (mg/dL)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'VD: 140'}))