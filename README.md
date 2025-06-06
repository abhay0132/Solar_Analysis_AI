# Rooftop Solar Potential Analysis Project

## Project Journey Overview

The goal of this project was to develop a tool to assess the solar potential of a house's rooftop using satellite imagery and AI vision, as part of an internship project to demonstrate AI applications in the solar industry. [cite_start]The tool was designed to analyze a rooftop image, estimate its area, calculate solar energy potential, and provide detailed recommendations for solar panel installation, including ROI and industry insights. The target location was Agra, India (coordinates 27.81, 78.8667), but challenges with satellite imagery and API access required adjustments to complete the project.

## Initial Steps

The project began with setting up the development environment and defining the tool's functionality. The plan was to fetch satellite imagery for the given coordinates, use an AI model (via OpenRouter and GPT-4o) to detect the rooftop, and then calculate solar potential using a custom algorithm. A Gradio interface was chosen to allow users to input coordinates and electricity rates and view the results.

## Virtual Environment Creation

1.  **Set Up a Virtual Environment**: To ensure a clean development environment, a virtual environment was created using the following commands:
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scripts\activate
    ```
2.  **Install Dependencies**: The required Python libraries were installed using pip: `pip install gradio requests Pillow`. These libraries were needed for the Gradio interface (`gradio`), API calls to OpenRouter (`requests`), and image processing (`Pillow`).

## Development Process

The main script, `app5.py`, was developed to handle the following tasks:

* Load a satellite image for the given coordinates.
* Use the OpenRouter API with GPT-4o to detect the rooftop and estimate its area.
* Calculate solar potential, including energy production, number of panels, installation cost, annual savings, and payback period.
* Generate detailed recommendations on solar panel technology, installation, maintenance, ROI, regulations, and market trends.
* Display the results through a Gradio interface.

The initial approach was to fetch satellite imagery dynamically using APIs like MapTiler, but challenges arose, leading to adjustments in the implementation.

## Project Structure

* `app5.py`: The main script containing the tool's logic, including image loading, rooftop detection, solar potential calculation, and Gradio interface.
* `images/`: A directory containing the satellite image (e.g., `27.81_78.8667.png` for Agra, India, or a sample image like `37.7749_-122.4194.png` for San Francisco).
* `README.txt`: The project documentation (this file).

## Challenges Faced

1.  **Satellite Imagery Issues**
    * **Objective**: The goal was to fetch high-resolution satellite imagery (approximately 1m/pixel) for Agra, India (coordinates 27.81, 78.8667) to analyze rooftops.
    * **Sources Tried**:
        * MapTiler: Encountered a `404 Client Error: Not Found`, even after correcting the URL structure. [cite_start]This was likely due to a lack of high-resolution imagery for Agra or restrictions in the free-tier plan.
        * Copernicus (Sentinel-2): Provided imagery at 10m resolution, which was too coarse to identify individual houses (houses appeared as 1-2 pixels).
        * Zoom Earth: The imagery was not clear enough at maximum zoom for Agra.
        * Bhuvan (ISRO): High-resolution imagery (e.g., Cartosat) was either unavailable or too unclear to use.
        * OpenAerialMap: No suitable imagery was found for the location.
    * **Solution**: Reverted to using a locally saved image placed in the `images/` directory (e.g., `27.81_78.8667.png`). As an alternative, a sample image from San Francisco (coordinates 37.7749, -122.4194) can be used to demonstrate the tool's functionality, saved as `images/37.7749_-122.4194.png`.

2.  **OpenRouter API Error Issue**: Encountered a `402 Client Error: Payment Required` when calling the OpenRouter API with the GPT-4o model for image analysis.
    * **Cause**: The free tier credits were exhausted due to multiple test requests, as image analysis consumes more credits than text-only requests.
    * **Solution**:
        * Recommended adding more credits to the OpenRouter account to proceed with real API calls.
        * For submission purposes, optionally mocked the API response in `app5.py` to demonstrate the tool's workflow. The mock response used was:
            ```python
            def detect_rooftop(image):
                mock_response = {
                    "total_area_m2": 120.00,
                    "description": "A rectangular rooftop with minimal obstructions, suitable for solar panels. Some shading from nearby trees may reduce efficiency.",
                    "confidence": 0.85
                }
                return image, mock_response["total_area_m2"], mock_response["description"], mock_response["confidence"]
            ```
            This mock response allows the tool to be evaluated without requiring live API access.

## Final Implementation

After facing the challenges above, the final implementation used a locally saved image (e.g., `27.81_78.8667.png`) instead of fetching satellite imagery dynamically. The `app5.py` script was updated to load the image from the `images/` directory, and the OpenRouter API call was optionally mocked to bypass the 402 error. The Gradio interface allows users to input coordinates (e.g., 27.81, 78.8667) and an electricity rate (e.g., 0.104 $/kWh), and the tool displays the image along with a detailed analysis, including rooftop area, solar potential, and recommendations.

The tool calculates solar potential based on the rooftop area (e.g., 120 m² from the mock response), assuming a solar efficiency of 20% (200 W/m²), and provides metrics like solar potential in kW, number of panels, annual energy production, installation cost, annual savings, and payback period. It also generates recommendations on solar panel technology, installation process, maintenance, cost analysis, industry regulations, and market trends.

## Future Improvements

* **Alternative Imagery Sources**: Integrate with other APIs, such as the Google Maps API, if budget permits, or explore using drone imagery for better resolution.
* **Cost Optimization**: Use lower-cost vision models on OpenRouter (e.g., LLAVA-13B) to reduce credit usage while still performing image analysis.
* **Enhanced Analysis**: Incorporate real solar irradiance data based on the location (e.g., using the NASA POWER API) to provide more accurate energy production estimates.
* **Image Preprocessing**: Add image enhancement techniques, such as contrast adjustment, to improve the accuracy of LLM detection for low-quality images.

## Project Outcome

The project was successfully completed despite the challenges, demonstrating the tool's functionality using a locally saved image and a mocked API response (if credits were unavailable). The final deliverable includes the `app2.py` script, an `images/` directory with the satellite image, and this documentation, ready for submission as part of the internship project. The tool showcases the potential of AI in the solar industry, even with the limitations encountered during development.

## Instructions for Use

Copy the entire content above into a file (e.g., `README.txt`) in your project directory (`Solar_Industry_AI/`).

### Project Structure

Ensure your project directory matches the structure described:
