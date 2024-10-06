import os
import streamlit as st
import folium
from streamlit_folium import st_folium
from supabase import create_client, Client
from folium.plugins import MarkerCluster
import uuid
import base64
from typing import List, Dict, Any

# Constants
SUPABASE_URL = "https://tijevatcuxldctpwwflh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRpamV2YXRjdXhsZGN0cHd3ZmxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgxMTM1NzksImV4cCI6MjA0MzY4OTU3OX0.KZiGvJK7jEYrxOIohAHxHey24iZCGd11o2eHqk4OMfg"
IMAGE_DIR = "uploaded_images"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def setup_page():
    st.set_page_config(layout="wide")
    st.title("E.A.R.T.H. - Environmental Action & Response Through Human-AI Technology")
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

def fetch_location_data() -> List[Dict[str, Any]]:
    try:
        response = supabase.table("locations").select("*").order('created_at', desc=True).execute()
        data = response.data
        if data:
            # Ensure latitude and longitude are floats
            for entry in data:
                entry['latitude'] = float(entry.get('latitude', 0.0))
                entry['longitude'] = float(entry.get('longitude', 0.0))
                entry['image_url'] = entry.get('image_url', None)
            return data
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def create_map(map_data: List[Dict[str, Any]]) -> folium.Map:
    m = folium.Map(location=[10, 75.0], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)

    for entry in map_data:
        name = entry.get('name', 'No Name')
        description = entry.get('description', 'No Description')
        latitude = entry.get('latitude', None)
        longitude = entry.get('longitude', None)
        image_url = entry.get('image_url', None)

        # Validate latitude and longitude
        if latitude is None or longitude is None:
            st.warning(f"Invalid location for entry: {name}. Skipping.")
            continue

        # Create popup content
        popup_content = f"<strong>{name}</strong><br>{description}<br>"
        if image_url:
            # Use the full path to the image
            full_image_path = os.path.abspath(image_url)
            # Use a data URI for the image
            with open(full_image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            popup_content += f'<img src="data:image/jpeg;base64,{img_data}" width="150px"/>'
        
        try:
            folium.Marker(
                [latitude, longitude],
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(marker_cluster)
        except Exception as e:
            st.error(f"Error adding marker: {e}")

    return m


def upload_image_locally(image) -> str:
    try:
        image_name = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join(IMAGE_DIR, image_name)
        # Create the file and write the image content
        with open(image_path, "wb") as f:
            f.write(image.getvalue())
        return image_path
    except Exception as e:
        st.error(f"Error uploading image: {e}")
        return ""

def insert_location(name: str, description: str, image_path: str, latitude: float, longitude: float) -> None:
    try:
        data = {
            "name": name,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
            "image_url": image_path
        }
        supabase.table("locations").insert(data).execute()
        st.success("Report added successfully!")
    except Exception as e:
        st.error(f"Error inserting data: {e}")

def add_new_marker():
    with st.form("add_marker_form"):
        name = st.text_input("Report Title")
        description = st.text_area("Description")
        image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0)
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0)

        if st.form_submit_button("Submit Report"):
            if all([name, description, image, latitude, longitude]):
                image_path = upload_image_locally(image)
                if image_path:
                    insert_location(name, description, image_path, latitude, longitude)
                    st.experimental_rerun()
            else:
                st.error("Please fill in all fields and upload an image.")

def display_recent_markers(map_data: List[Dict[str, Any]]):
    if map_data:
        for entry in map_data[:5]:
            st.markdown(f"**{entry.get('name', 'No Name')}**")
            st.write(entry.get('description', 'No Description'))
            st.image(entry.get('image_url', None), width=200)
            st.markdown("---")
    else:
        st.write("No recent reports found.")

def main():
    setup_page()
    
    col1, col2 = st.columns([3,1])

    with col1:
        map_data = fetch_location_data()
        m = create_map(map_data)
        st_folium(m, width=725)

    with col2:
        st.header("Recent Reports")
        display_recent_markers(map_data)

    with st.sidebar:
        st.header("Add a New Report")
        add_new_marker()

if __name__ == "__main__":
    main()
