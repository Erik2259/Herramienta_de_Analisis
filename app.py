import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Herramienta de Análisis - Etapa 1",
    page_icon="📊",
    layout="wide"
)

st.title("📊 1ra Etapa: Carga y Análisis de Datos")
st.markdown("---")

# ==========================================
# MÓDULO: CARGA DE ARCHIVOS CSV
# ==========================================
st.sidebar.header("Configuración de Entrada")
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Carga inicial del dataframe
        df = pd.read_csv(uploaded_file)
        st.success(f"Archivo '{uploaded_file.name}' cargado exitosamente.")
        
        # ==========================================
        # MÓDULO: VALIDACIÓN DEL ARCHIVO
        # ==========================================
        st.header("🛡️ Validación de Estructura")
        
        # Reglas básicas de validación
        es_valido = True
        errores = []
        
        if df.empty:
            es_valido = False
            errores.append("El archivo CSV está vacío.")
        if len(df.columns) < 1:
            es_valido = False
            errores.append("El archivo debe contener al menos una columna.")
            
        if es_valido:
            st.info("✅ El archivo cumple con la estructura básica requerida (No vacío y con columnas legibles).")
            
            # Vista previa de los datos
            with st.expander("Ver vista previa de los datos (Primeras 5 filas)"):
                st.dataframe(df.head())
                
            st.markdown("---")
            
            # ==========================================
            # MÓDULO: ANÁLISIS DESCRIPTIVO
            # ==========================================
            st.header("📈 Análisis Descriptivo Básicos")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Número de Filas", value=df.shape[0])
            with col2:
                st.metric(label="Número de Columnas", value=df.shape[1])
                
            # Tipos de datos y nulos por columna
            st.subheader("Estructura de Columnas y Datos Faltantes")
            info_df = pd.DataFrame({
                "Tipo de Dato": df.dtypes.astype(str),
                "Valores Nulos": df.isnull().sum(),
                "Porcentaje Nulos (%)": (df.isnull().sum() / len(df) * 100).round(2),
                "Valores Únicos": df.nunique()
            })
            st.dataframe(info_df, use_container_width=True)
            
            # Estadísticas descriptivas detalladas
            st.subheader("Estadísticas Descriptivas Avanzadas")
            
            # Separar numéricas de categóricas para análisis correcto
            num_cols = df.select_dtypes(include=['number']).columns
            
            if len(num_cols) > 0:
                # Calcular métricas explícitas solicitadas
                stats_summary = pd.DataFrame(index=["Mínimo", "Máximo", "Media", "Mediana", "Moda"])
                
                for col in num_cols:
                    # La moda puede devolver múltiples valores, tomamos el primero
                    moda_val = df[col].mode().iloc[0] if not df[col].mode().empty else None
                    stats_summary[col] = [
                        df[col].min(),
                        df[col].max(),
                        df[col].mean(),
                        df[col].median(),
                        moda_val
                    ]
                
                st.markdown("**Variables Numéricas (Mín, Máx, Media, Mediana, Moda):**")
                st.dataframe(stats_summary, use_container_width=True)
            else:
                st.warning("No se detectaron columnas numéricas para calcular estadísticas avanzadas.")
                
            st.markdown("---")
            
            # ==========================================
            # MÓDULO: GRÁFICAS (MAPA DE CALOR)
            # ==========================================
            st.header("🎨 Visualización y Gráficas")
            
            tab1, tab2 = st.tabs(["Mapa de Calor (Correlación)", "Mapa de Calor (Datos Faltantes)"])
            
            with tab1:
                st.subheader("Matriz de Correlación")
                if len(num_cols) > 1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    corr_matrix = df[num_cols].corr()
                    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5)
                    st.pyplot(fig)
                else:
                    st.warning("Se necesitan al menos 2 columnas numéricas para generar una matriz de correlación.")
                    
            with tab2:
                st.subheader("Matriz de Valores Faltantes (Nulos)")
                fig, ax = plt.subplots(figsize=(10, 5))
                # Si no hay nulos, se mostrará un mapa uniforme continuo
                sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False, ax=ax)
                st.pyplot(fig)
                
        else:
            st.error("❌ El archivo no cumple con las condiciones estructurales:")
            for err in errores:
                st.write(f"- {err}")
                
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Por favor, carga un archivo CSV desde la barra lateral para iniciar el análisis.")