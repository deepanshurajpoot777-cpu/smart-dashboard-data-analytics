# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# #page setup
# st.set_page_config(layout="wide")
# st.title("Smart Dashboard Data Analytics")

# # upload file
# file=st.file_uploader("Upload CSV file")

# if file:
#     try:
#        df=pd.read_csv(file)
#        #---------------------matrics---------------
#        col1,col2,col3=st.columns(3)
#        col1.metric("Rows",df.shape[0])
#        col2.metric("Columns",df.shape[1])
#        col3.metric("Missing Values",int(df.isnull().sum().sum()))
    
#     # --------------------data preview-------------------------------
#        st.subheader("📃 Data Preview")
#        st.dataframe(df)
    
#     #-----------------------Data info--------------------------
#        st.subheader("📌 Dataset Information")
#        c1,c2=st.columns(2)
#        with c1:
           
#            st.write("**shape**",df.shape)
#            st.write("**Data Types:**")
#            st.write(df.dtypes)
#        with c2:
           
#            st.write("**Missing Values**")
#            st.write(df.isnull().sum())
    
#         # ---------------------Detect coloumn--------------------------
#        numeric_cols=df.select_dtypes(include='number').columns.tolist()
    
#         # sidebar controls
#        st.sidebar.header("Controls")
#        char_type=st.sidebar.selectbox(
#             "Select Chart Type",
            
#             ["Bar Chart","Line Chart","Pie Chart","Histogram"]
#         )
#         # Select Coloumn
#        x_col=st.sidebar.selectbox("Select X-axis",df.columns)
    
#        if numeric_cols:
    
#             y_col=st.sidebar.selectbox("Select Y-axis",numeric_cols)
    
    
#             st.subheader("📊 Visulization")
    
#             # Bar Chart
#             if char_type=="Bar Chart":
#                 st.bar_chart(df[[x_col,y_col]].set_index(x_col))
    
#             # Line Chart

#             elif char_type=="Line Chart":
#                 st.line_chart(df[[x_col,y_col]].set_index(x_col))

#             #pie chart(Fixed clean version)

#             elif char_type=="Pie Chart":
#                 pie_data=df.groupby(x_col)[y_col].sum().dropna()
    
#                 fig,ax=plt.subplots(figsize=(5,5))
#                 ax.pie(
#                     pie_data,
#                     labels=pie_data.index,
#                     autopct="%1.1f%%",
#                     startangle=90,
#                     pctdistance=0.8
#                 )
#                 ax.axis("equal")
#                 st.pyplot(fig)
#             # Histogram
#             elif char_type=="Histogram":
#                 st.bar_chart(df[y_col].value_counts())
            
#             # statics
#             st.subheader("📈 Statistics")
#             st.write(df[y_col].describe())

#             #------------------------DOWNLOAD CSV-------------------------
#             st.download_button("Download csv",df.to_csv(index=False),"cleaned data csv","txt/csv")
    
#        else:
#             st.warning("No numeric columns found in data")
#     except Exception as e:
#         st.error(f"❌ Error reading file: {e}")
    
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# PAGE SETUP
# ==========================================================

st.set_page_config(
    page_title="Smart Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Dashboard Data Analytics")
st.caption("Upload a CSV file and explore, analyze and visualize your data.")

# ==========================================================
# UPLOAD FILE
# ==========================================================

file = st.file_uploader(
    "📂 Upload CSV file",
    type=["csv"]
)

if file:

    try:

        # Read CSV
        df = pd.read_csv(file)

        # ==================================================
        # SIDEBAR
        # ==================================================

        st.sidebar.header("⚙️ Controls")

        # ==================================================
        # BASIC INFORMATION
        # ==================================================

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        duplicate_rows = df.duplicated().sum()
        missing_values = int(df.isnull().sum().sum())

        # ==================================================
        # METRICS
        # ==================================================

        st.subheader("📌 Dataset Overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Rows",
            df.shape[0]
        )

        col2.metric(
            "Columns",
            df.shape[1]
        )

        col3.metric(
            "Missing Values",
            missing_values
        )

        col4.metric(
            "Duplicate Rows",
            duplicate_rows
        )

        col5.metric(
            "Numeric Columns",
            len(numeric_cols)
        )

        # ==================================================
        # DATA PREVIEW
        # ==================================================

        st.subheader("📃 Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==================================================
        # DATA INFORMATION
        # ==================================================

        st.subheader("📌 Dataset Information")

        c1, c2 = st.columns(2)

        with c1:

            st.write("**Shape:**", df.shape)

            st.write("**Data Types:**")

            st.dataframe(
                df.dtypes.astype(str).to_frame("Data Type"),
                use_container_width=True
            )

        with c2:

            st.write("**Missing Values:**")

            missing_df = df.isnull().sum().to_frame(
                "Missing Values"
            )

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        # ==================================================
        # SEARCH
        # ==================================================

        st.sidebar.subheader("🔎 Search")

        search = st.sidebar.text_input(
            "Search in dataset"
        )

        if search:

            filtered_df = df[
                df.astype(str)
                .apply(
                    lambda row:
                    row.str.contains(
                        search,
                        case=False,
                        na=False
                    ).any(),
                    axis=1
                )
            ]

            st.subheader("🔎 Search Results")

            st.write(
                f"Found **{len(filtered_df)}** matching rows."
            )

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

        # ==================================================
        # DATA CLEANING
        # ==================================================

        st.sidebar.subheader("🧹 Data Cleaning")

        remove_duplicates = st.sidebar.checkbox(
            "Remove Duplicate Rows"
        )

        if remove_duplicates:

            df = df.drop_duplicates()

            st.success(
                "✅ Duplicate rows removed."
            )

        # Missing value handling

        missing_option = st.sidebar.selectbox(
            "Missing Value Handling",
            [
                "None",
                "Drop Rows",
                "Fill Numeric with Mean"
            ]
        )

        if missing_option == "Drop Rows":

            df = df.dropna()

            st.success(
                "✅ Rows containing missing values removed."
            )

        elif missing_option == "Fill Numeric with Mean":

            for col in numeric_cols:

                df[col] = df[col].fillna(
                    df[col].mean()
                )

            st.success(
                "✅ Missing numeric values filled with mean."
            )

        # ==================================================
        # VISUALIZATION CONTROLS
        # ==================================================

        st.sidebar.subheader("📊 Visualization")

        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Histogram",
                "Scatter Plot",
                "Box Plot"
            ]
        )

        # X-axis

        x_col = st.sidebar.selectbox(
            "Select X-axis",
            df.columns
        )

        # ==================================================
        # NUMERIC COLUMN CHECK
        # ==================================================

        if numeric_cols:

            y_col = st.sidebar.selectbox(
                "Select Y-axis",
                numeric_cols
            )

            # ==================================================
            # VISUALIZATION
            # ==================================================

            st.subheader("📊 Visualization")

            # ---------------- BAR ----------------

            if chart_type == "Bar Chart":

                chart_data = (
                    df.groupby(x_col)[y_col]
                    .sum()
                    .sort_values(ascending=False)
                    .head(20)
                )

                st.bar_chart(
                    chart_data
                )

            # ---------------- LINE ----------------

            elif chart_type == "Line Chart":

                st.line_chart(
                    df[[x_col, y_col]]
                    .set_index(x_col)
                )

            # ---------------- PIE ----------------

            elif chart_type == "Pie Chart":

                pie_data = (
                    df.groupby(x_col)[y_col]
                    .sum()
                    .dropna()
                    .sort_values(
                        ascending=False
                    )
                    .head(10)
                )

                fig, ax = plt.subplots(
                    figsize=(6, 6)
                )

                ax.pie(
                    pie_data,
                    labels=pie_data.index,
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.axis("equal")

                st.pyplot(fig)

            # ---------------- HISTOGRAM ----------------

            elif chart_type == "Histogram":

                fig, ax = plt.subplots()

                ax.hist(
                    df[y_col].dropna(),
                    bins=20
                )

                ax.set_xlabel(y_col)
                ax.set_ylabel("Frequency")
                ax.set_title(
                    f"Distribution of {y_col}"
                )

                st.pyplot(fig)

            # ---------------- SCATTER ----------------

            elif chart_type == "Scatter Plot":

                fig, ax = plt.subplots()

                ax.scatter(
                    df[x_col],
                    df[y_col]
                )

                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

                ax.set_title(
                    f"{x_col} vs {y_col}"
                )

                st.pyplot(fig)

            # ---------------- BOX PLOT ----------------

            elif chart_type == "Box Plot":

                fig, ax = plt.subplots()

                ax.boxplot(
                    df[y_col].dropna()
                )

                ax.set_ylabel(y_col)

                ax.set_title(
                    f"Box Plot - {y_col}"
                )

                st.pyplot(fig)

            # ==================================================
            # STATISTICS
            # ==================================================

            st.subheader("📈 Statistics")

            stats = df[y_col].describe()

            st.dataframe(
                stats.to_frame(
                    name=y_col
                ),
                use_container_width=True
            )

        else:

            st.warning(
                "⚠️ No numeric columns found in data."
            )

        # ==================================================
        # CORRELATION ANALYSIS
        # ==================================================

        if len(numeric_cols) >= 2:

            st.subheader("🔥 Correlation Analysis")

            correlation = df[numeric_cols].corr()

            fig, ax = plt.subplots(
                figsize=(10, 6)
            )

            sns.heatmap(
                correlation,
                annot=True,
                fmt=".2f",
                ax=ax
            )

            ax.set_title(
                "Correlation Heatmap"
            )

            st.pyplot(fig)

        # ==================================================
        # CATEGORICAL ANALYSIS
        # ==================================================

        if categorical_cols:

            st.subheader(
                "📋 Categorical Column Analysis"
            )

            selected_cat = st.selectbox(
                "Select Categorical Column",
                categorical_cols
            )

            value_counts = (
                df[selected_cat]
                .value_counts()
                .head(20)
            )

            st.bar_chart(
                value_counts
            )

        # ==================================================
        # DOWNLOAD CSV
        # ==================================================

        st.subheader("📥 Download Dataset")

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except Exception as e:

        st.error(
            f"❌ Error reading file: {e}"
        )

else:

    st.info(
        "👆 Please upload a CSV file to start analyzing."
    )
    