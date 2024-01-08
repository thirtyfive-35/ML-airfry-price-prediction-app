import streamlit as st
import pandas as pd
import joblib

# Eğitilmiş modeli yükle
model = joblib.load("GradientBoostingRegressorModel5.pkl")

def map_categorical_values(user_input):
    # Kategorik değerleri dönüştür
    user_input['Çıkarılabilir_Hazne'] = user_input['Çıkarılabilir_Hazne'].map({'Yok': 0, 'Var': 1})
    user_input['Zamanlayıcı'] = user_input['Zamanlayıcı'].map({'Yok': 0, 'Var': 1})
    user_input['Hazne_Sayısı'] = user_input['Hazne_Sayısı'].map({'Tek': 1, 'Çift': 0})
    user_input['Türü'] = user_input['Türü'].map({'Yağsız_Airfryer': 1, 'Yağlı': 0})
    user_input['Kontrol_Paneli'] = user_input['Kontrol_Paneli'].map({'Dokunmatik': 1, 'Mekanik': 0})

    # Kapasite değerlerini sayısal bir forma çevir
    capacity_mapping = {
        '6 lt ve Üzeri': 6,
        '5 - 5,9 lt': 5,
        '0,9 lt ve Altı': 0,
        '4 - 4,9 lt': 4,
        '3 - 3,9 lt': 3,
        '2 - 2,9 lt': 2,
        '1 - 1,9 lt': 1
    }
    user_input['Kapasite'] = user_input['Kapasite'].map(capacity_mapping)

    return user_input

def predict_price(model, user_input, selected_brand):
    user_input = map_categorical_values(user_input)

    # Seçilen markayı one-hot formatına çevir
    brand_columns = [f'marka_{brand}' for brand in ["Arçelik", "Diğer", "Goldmaster", "Karaca", "Kenwood", "Kiwi", "Kumtel", "Onvo", "Philips", "Schafer", "Tefal", "Wiami", "Xiaomi", "Yasomi"]]
    user_input[brand_columns] = 0
    user_input[f'marka_{selected_brand}'] = 1

    # Modelin eğitildiği sütun isimlerini al
    model_features = list(user_input.columns)

    return model.predict(user_input[model_features])[0]

def main():
    st.title('Ürün Fiyatı Tahmini 👨‍💻')

    # Kullanıcıdan girişleri al
    power = st.number_input('Güç_W', min_value=0)
    removable_bin = st.radio('Çıkarılabilir_Hazne', ['Yok', 'Var'])  # 0: Yok, 1: Var
    timer = st.radio('Zamanlayıcı', ['Yok', 'Var'])  # 0: Yok, 1: Var
    capacity = st.radio('Kapasite', ['6 lt ve Üzeri', '5 - 5,9 lt', '0,9 lt ve Altı', '4 - 4,9 lt', '3 - 3,9 lt', '2 - 2,9 lt', '1 - 1,9 lt'])
    bin_count = st.radio('Hazne_Sayısı', ['Tek', 'Çift'])  # 1 veya 2
    airfry_type = st.radio('Türü', ['Yağsız_Airfryer', 'Yağlı'])
    control_panel = st.radio('Kontrol_Paneli', ['Dokunmatik', 'Mekanik'])

    # Kullanıcının girdiği verileri bir DataFrame'e dönüştür
    user_input = pd.DataFrame({
        'Güç_W': [power],
        'Çıkarılabilir_Hazne': [removable_bin],
        'Zamanlayıcı': [timer],
        'Kapasite': [capacity],
        'Hazne_Sayısı': [bin_count],
        'Türü': [airfry_type],
        'Kontrol_Paneli': [control_panel]
    })

    selected_brand = st.selectbox('Marka Seçiniz..', ["Arçelik", "Diğer", "Goldmaster", "Karaca", "Kenwood", "Kiwi", "Kumtel", "Onvo", "Philips", "Schafer", "Tefal", "Wiami", "Xiaomi", "Yasomi"])

    if st.button("Tahmin Yap"):
        result = predict_price(model, user_input, selected_brand)
        st.success('Tahmin Başarılı')
        st.write("Tahmin Edilen Fiyat: {:.3f} TL".format(result))

if __name__ == "__main__":
    main()
