# Rooftop Solar Analysis Tool using OpenRouter API and Local Imagery
import gradio as gr
import requests
from PIL import Image
import base64
from io import BytesIO
import json
import math
import os

# API keys
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"  # Placeholder for API key

# Define the path to the images directory (relative path for portability)
IMAGE_DIR = "./images"

# Function to load pre-downloaded satellite image
def load_local_image(lat, lon, size="640x640"):
    """
    Loads a pre-downloaded satellite image based on latitude and longitude.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        size (str): Desired image size in "widthxheight" format.
    Returns:
        PIL.Image: Resized image.
    Raises:
        Exception: If image file is not found.
    """
    filename = os.path.join(IMAGE_DIR, f"{lat}_{lon}.png")
    if not os.path.exists(filename):
        raise Exception(f"No image found for coordinates {lat}, {lon} at {filename}. Please download satellite imagery for this location.")
    image = Image.open(filename)
    width, height = map(int, size.split("x"))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    return image

# Function to encode image to base64
def image_to_base64(image):
    """
    Converts an image to base64 format for OpenRouter API.
    Args:
        image (PIL.Image): Image to encode.
    Returns:
        str: Base64-encoded string.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to analyze rooftop using OpenRouter API (e.g., GPT-4o)
def detect_rooftop(image):
    """
    Uses OpenRouter API to analyze the image for rooftops.
    Args:
        image (PIL.Image): Satellite image to analyze.
    Returns:
        tuple: (image, total_area_m2, description, confidence).
    Raises:
        Exception: If API call fails or response is invalid.
    """
    base64_image = image_to_base64(image)
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this satellite image (1m resolution) for a rooftop suitable for solar panel installation. "
                            "Look for distinct rectangular or polygonal shapes that indicate building rooftops, avoiding areas with vegetation or irregular terrain. "
                            "Estimate the rooftop area in square meters (assume 1m/pixel). "
                            "Return a JSON object with: "
                            "- `total_area_m2`: Estimated rooftop area in square meters (numeric, rounded to 2 decimal places). "
                            "- `description`: Brief description of the rooftop (e.g., shape, obstructions, clarity of detection, max 100 words). "
                            "- `confidence`: Confidence score (0-1) for the detection accuracy. "
                            "If no rooftop is detected, return `total_area_m2` as 0, set `confidence` to 0, and explain why in `description` (e.g., image too unclear, no distinct rooftops)."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API error: {str(e)}")
    
    result = response.json()
    try:
        content = result["choices"][0]["message"]["content"]
        analysis = json.loads(content)
        if not all(key in analysis for key in ["total_area_m2", "description", "confidence"]):
            raise KeyError("Missing required keys in OpenRouter response")
        return image, float(analysis["total_area_m2"]), analysis["description"], float(analysis["confidence"])
    except (json.JSONDecodeError, KeyError) as e:
        raise Exception(f"Failed to parse OpenRouter response: {str(e)}")

# Calculate solar potential and ROI
def calculate_solar_potential(area_m2, lat, lon, electricity_rate=0.12):
    """
    Calculates solar potential, installation details, and ROI.
    Args:
        area_m2 (float): Rooftop area in square meters.
        lat (float): Latitude (for context, not used in calc).
        lon (float): Longitude (for context, not used in calc).
        electricity_rate (float): Electricity rate in $/kWh.
    Returns:
        dict: Solar potential, installation, and ROI metrics.
    """
    solar_efficiency = 0.2  # 200 W/m²
    solar_potential_kw = area_m2 * solar_efficiency
    
    panel_area = 1.6  # m² per panel (400W panel)
    num_panels = int(area_m2 // panel_area) if area_m2 > 0 else 0
    
    annual_energy_kwh = solar_potential_kw * 4 * 365
    
    installation_cost = solar_potential_kw * 1500
    annual_savings = annual_energy_kwh * electricity_rate
    payback_period = installation_cost / annual_savings if annual_savings > 0 else float('inf')
    
    return {
        "solar_potential_kw": round(solar_potential_kw, 2),
        "num_panels": num_panels,
        "annual_energy_kwh": round(annual_energy_kwh, 2),
        "installation_cost": round(installation_cost, 2),
        "annual_savings": round(annual_savings, 2),
        "payback_period_years": round(payback_period, 2)
    }

# Generate detailed recommendations
def generate_recommendations(area_m2, results, electricity_rate, confidence):
    """
    Generates detailed recommendations for solar installation.
    Args:
        area_m2 (float): Rooftop area in square meters.
        results (dict): Solar potential and ROI metrics.
        electricity_rate (float): Electricity rate in $/kWh.
        confidence (float): Confidence score from LLM.
    Returns:
        str: Detailed recommendations.
    """
    if area_m2 == 0:
        return (
            "No suitable rooftop detected for solar installation. Consider the following:\n"
            "- Verify the image clarity or try a different location with better visibility.\n"
            "- Ensure the area has distinct rooftops, not obscured by vegetation or terrain.\n"
            "- Alternatively, consult a local solar professional for an on-site assessment."
        )
    
    panel_info = (
        "Recommended Solar Panels: Monocrystalline panels (e.g., 400W, 20% efficiency).\n"
        "- Efficiency: 20% (200 W/m²).\n"
        "- Panel Size: ~1.6 m² per panel.\n"
        "- Advantages: High efficiency, long lifespan (25+ years), performs well in low light."
    )
    
    installation_info = (
        "Installation Process:\n"
        "- **Mounting**: Use racking systems compatible with your roof type (e.g., asphalt shingle, metal).\n"
        "- **Electrical**: Requires an inverter (string or microinverters) and connection to the grid.\n"
        "- **Permits**: Obtain local building permits and utility interconnection agreements.\n"
        "- **Timeline**: Typically 1-2 weeks"
    )
    
    maintenance_info = (
        "Maintenance Requirements:\n"
        "- **Monitoring**: Install a monitoring system to track energy production.\n"
        "- **Cleaning**: Clean panels 1-2 times/year to remove dust/debris (use soft brushes, water).\n"
        "- **Warranties**: Panels typically come with 25-year performance warranties; inverters 5-10 years."
    )
    
    roi_info = (
        f"Cost & ROI Analysis:\n"
        f"- **Installation Cost**: ${results['installation_cost']} (estimated at $1,500/kW).\n"
        f"- **Annual Energy Production**: {results['annual_energy_kwh']} kWh.\n"
        f"- **Annual Savings**: ${results['annual_savings']} at ${electricity_rate}/kWh.\n"
        f"- **Payback Period**: {results['payback_period_years']} years.\n"
        f"- **Incentives**: Check for local incentives (e.g., tax credits, rebates, net metering in India)."
    )
    
    regulation_info = (
        "Industry Regulations:\n"
        "- **Codes**: Comply with local building codes (e.g., IS 875 for structural safety in India).\n"
        "- **Net Metering**: Available in India; excess energy can be sold back to the grid.\n"
        "- **Safety**: Ensure proper grounding, use certified installers (e.g., MNRE-approved in India)."
    )
    
    market_info = (
        "Market Trends (2025):\n"
        "- **Technology Advances**: Bifacial panels and energy storage (e.g., Tesla Powerwall) are gaining popularity.\n"
        "- **Adoption Rates**: Solar adoption in India is growing at ~15% annually, driven by government initiatives (e.g., PM Surya Ghar Yojana).\n"
        "- **Cost Decline**: Solar panel costs have dropped ~20% since 2023, making installations more affordable."
    )
    
    confidence_info = (
        f"Analysis Confidence: {confidence:.2f}\n"
        "- Note: Confidence below 0.8 may indicate unclear imagery or complex rooftop structures. Consider an on-site inspection for accuracy."
    )
    
    return (
        f"**Rooftop Solar Potential Analysis**\n\n"
        f"**Rooftop Area Detected**: {area_m2} m²\n"
        f"**Number of Panels**: {results['num_panels']}\n"
        f"**Solar Potential**: {results['solar_potential_kw']} kW\n\n"
        f"**Solar Panel Technology**\n{panel_info}\n\n"
        f"**Installation Process**\n{installation_info}\n\n"
        f"**Maintenance Requirements**\n{maintenance_info}\n\n"
        f"**Cost & ROI Analysis**\n{roi_info}\n\n"
        f"**Industry Regulations**\n{regulation_info}\n\n"
        f"**Market Trends**\n{market_info}\n\n"
        f"**Analysis Confidence**\n{confidence_info}"
    )

# Main function for Gradio interface
def analyze_rooftop(lat, lon, electricity_rate=0.12):
    """
    Analyzes a rooftop for solar potential using satellite imagery.
    Args:
        lat (str): Latitude as a string.
        lon (str): Longitude as a string.
        electricity_rate (float): Electricity rate in $/kWh.
    Returns:
        tuple: (image, recommendations) or (None, error message).
    """
    try:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError("Invalid coordinates: Latitude must be between -90 and 90, Longitude between -180 and 180.")
        
        image = load_local_image(lat, lon)
        
        output_image, total_area_m2, description, confidence = detect_rooftop(image)
        
        results = calculate_solar_potential(total_area_m2, lat, lon, electricity_rate)
        
        recommendations = generate_recommendations(total_area_m2, results, electricity_rate, confidence)
        
        recommendations = f"**Rooftop Description**: {description}\n\n{recommendations}"
        
        return output_image, recommendations
    
    except Exception as e:
        return None, f"Error: {str(e)}"

# Gradio interface
iface = gr.Interface(
    fn=analyze_rooftop,
    inputs=[
        gr.Textbox(label="Latitude", placeholder="e.g., 27.7778"),
        gr.Textbox(label="Longitude", placeholder="e.g., 78.8667"),
        gr.Slider(minimum=0.05, maximum=0.5, value=0.12, label="Electricity Rate ($/kWh)")
    ],
    outputs=[
        gr.Image(label="Rooftop Analysis"),
        gr.Textbox(label="Recommendations")
    ],
    title="Rooftop Solar Potential Analysis",
    description="Enter your location and electricity rate to assess your rooftop's solar potential using AI vision."
)

# Launch the interface
if __name__ == "__main__":
    iface.launch()