import pandas as pd
import streamlit as st
import io

def main():
    st.title("🪶 Feather to CSV Converter")
    st.write("Upload a feather file to convert it to CSV format")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a feather file", 
        type=['feather'],
        help="Select a .feather file to convert to CSV"
    )
    
    if uploaded_file is not None:
        try:
            # Read the feather file
            df = pd.read_feather(uploaded_file)
            
            # Display basic info about the dataset
            st.success(f"✅ File loaded successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Show column info
            st.subheader("📊 Dataset Overview")
            st.write("**Column Information:**")
            
            # Create a summary of columns
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Preview the data
            st.subheader("👀 Data Preview")
            
            # Allow user to choose number of rows to preview
            preview_rows = st.slider("Number of rows to preview:", 1, min(50, len(df)), 10)
            st.dataframe(df.head(preview_rows), use_container_width=True)
            
            # Convert to CSV
            st.subheader("💾 Download CSV")
            
            # Convert dataframe to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            # Generate filename
            original_name = uploaded_file.name
            csv_filename = original_name.rsplit('.', 1)[0] + '.csv'
            
            # Download button
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=csv_filename,
                mime='text/csv',
                help=f"Download the converted file as {csv_filename}"
            )
            
            # Show conversion info
            st.info(f"🔄 Ready to download **{csv_filename}** ({len(csv_data):,} characters)")
            
        except Exception as e:
            st.error(f"❌ Error reading feather file: {str(e)}")
            st.write("Please make sure the uploaded file is a valid feather file.")
    
    else:
        st.info("👆 Please upload a feather file to get started")
        
        # Add some helpful information
        with st.expander("ℹ️ About Feather Format"):
            st.write("""
            **Feather** is a fast, lightweight, and easy-to-use binary columnar serialization format.
            
            **Advantages of Feather:**
            - Very fast read/write operations
            - Preserves data types
            - Cross-language compatibility (Python, R, etc.)
            - Efficient storage
            
            **When to convert to CSV:**
            - Need compatibility with tools that don't support feather
            - Want human-readable format
            - Need to import into Excel or other spreadsheet applications
            """)

if __name__ == "__main__":
    main()
