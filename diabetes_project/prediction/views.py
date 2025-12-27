import os
import joblib
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.conf import settings
from .forms import DiabetesForm

# Load models một lần khi khởi động server để tối ưu tốc độ
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models/best_logistic_model.joblib')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_models/scaler.joblib')
COLUMNS_PATH = os.path.join(settings.BASE_DIR, 'ml_models/model_columns.joblib')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
model_columns = joblib.load(COLUMNS_PATH)


def preprocess_input(data, model_cols, scaler_obj):
    """
    Hàm này chuyển đổi dữ liệu nhập từ form thành định dạng 
    chính xác mà mô hình yêu cầu (giống hệt lúc train).
    """
    # 1. Tạo DataFrame từ dữ liệu nhập
    df = pd.DataFrame([data])

    # 2. Scale các biến số (Thứ tự phải đúng như lúc fit scaler)
    numerical_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    df[numerical_cols] = scaler_obj.transform(df[numerical_cols])

    # 3. One-Hot Encoding (Thủ công để đảm bảo đúng cột)
    # Tạo các cột dummy với giá trị 0
    df_processed = pd.DataFrame(columns=model_cols)
    df_processed.loc[0] = 0  # Khởi tạo hàng đầu tiên là 0

    # Gán các giá trị số đã scale
    for col in numerical_cols:
        df_processed.at[0, col] = df.at[0, col]

    # Gán giá trị binary
    df_processed.at[0, 'hypertension'] = int(data['hypertension'])
    df_processed.at[0, 'heart_disease'] = int(data['heart_disease'])

    # Gán giá trị One-Hot cho Gender
    # Logic: Nếu chọn Male thì cột 'gender_Male' = 1, v.v.
    # Lưu ý: drop_first=True trong notebook đã bỏ cột 'gender_Female'
    if f"gender_{data['gender']}" in df_processed.columns:
        df_processed.at[0, f"gender_{data['gender']}"] = 1

    # Gán giá trị One-Hot cho Smoking
    if f"smoking_history_{data['smoking_history']}" in df_processed.columns:
        df_processed.at[0, f"smoking_history_{data['smoking_history']}"] = 1

    # Đảm bảo đúng thứ tự cột
    return df_processed[model_cols]


def predict_view(request):
    result = None
    probability = None

    if request.method == 'POST':
        form = DiabetesForm(request.POST)
        if form.is_valid():
            try:
                # Lấy dữ liệu sạch từ form
                input_data = form.cleaned_data

                # Tiền xử lý dữ liệu
                processed_data = preprocess_input(input_data, model_columns, scaler)

                # Dự đoán
                prediction = model.predict(processed_data)[0]
                proba = model.predict_proba(processed_data)[0][1]  # Xác suất bị bệnh

                result = "Nguy cơ cao (Dương tính)" if prediction == 1 else "An toàn (Âm tính)"
                probability = round(proba * 100, 2)

            except Exception as e:
                result = f"Lỗi xử lý: {str(e)}"
    else:
        form = DiabetesForm()

    return render(request, 'prediction/index.html', {
        'form': form,
        'result': result,
        'probability': probability
    })