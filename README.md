# Solar_Analysis_AI
# 🌞 Solar Industry AI Assistant

This AI-powered tool assesses the solar potential of a house’s rooftop using satellite imagery and AI vision. It analyzes a rooftop image to estimate its area, calculates solar energy potential, and provides detailed recommendations for solar panel installation, including ROI and industry insights.

## 🚀 Features

- **Rooftop Detection:** Identifies a rooftop in a satellite image and estimates its area in square meters.
- **Solar Potential Calculation:** Estimates solar energy production, number of panels, installation cost, annual savings, and payback period.
- **Recommendations:** Provides insights on:
  - Solar panel technology
  - Installation processes
  - Maintenance
  - ROI analysis
  - Regulations
  - Market trends.
- **User Interface:** Gradio interface for easy input of location coordinates and electricity rate, with results displayed in a clear format.

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Virtual Environment (recommended)

### Dependencies

- `gradio`: For the user interface
- `requests`: For API calls (if OpenRouter is used)
- `Pillow`: For image processing

### Installation

1. Clone the Repository:
   ```bash
   git clone https://github.com/your-username/solar-industry-ai.git
   cd solar-industry-ai
