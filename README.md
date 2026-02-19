# Eco Waste SA: Smart Reporting for Sustainable Communities

A centralized platform designed to tackle South Africa's waste crisis through community-driven action, AI-powered intelligence, and education. This project was developed by **Team GreenDelta** for the **UNISA Code the Climate Hackathon**.

## 🌍 The Problem

South Africa faces a critical waste management crisis characterized by overwhelmed systems and widespread illegal dumping. Landfills are significant contributors to climate change, producing landfill gas (LFG) composed of roughly 50% methane and 50% carbon dioxide as organic materials decompose in anaerobic environments.

## 💡 Our Solution

**Eco Waste SA** is a user-friendly platform that empowers citizens to report environmental issues and provides municipalities with the data needed for effective intervention.

### Key Features

* 
**Report**: Citizens can easily report illegal dumping by uploading photos, categorizing waste, and dropping a location pin.


* 
**Interactive Community Map**: A transparent, real-time map showing all reported incidents to foster community awareness.


* 
**AI-Powered Analytics**: A dashboard for municipalities that transforms citizen reports into actionable intelligence for proactive resource allocation.


* 
**The Learning Hub**: Integrated educational courses that teach users about recycling, composting, and waste reduction to address the root causes of the waste crisis.



## 🛠️ Technology Stack

* **Web Framework**: Flask (Python)
* **Frontend**: HTML, CSS, JavaScript
* 
**Backend & Database**: Azure App Service and Azure SQL Database 


* **AI & Geospatial Services**:
* 
**Azure Computer Vision**: Automatically analyzes images to categorize waste and estimate volume.


* 
**Azure Maps**: Powers the interactive reporting map and provides location data.


* 
**Power BI Embedded**: Visualizes real-time trends and metrics for municipality dashboards.





## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Flask
* Azure Account (for AI services and database)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-repo/eco-waste-sa.git
cd eco-waste-sa

```


```


3. **Set up environment variables**:
Create a `.env` file and add your Azure credentials and Flask secret keys:
```env
AZURE_CV_KEY=your_key
AZURE_MAPS_KEY=your_key
DATABASE_URL=your_sql_db_connection_string

```


4. **Run the application**:
```bash
flask run

```



## 📈 Impact & Vision

* 
**Short-Term**: Foster cleaner communities and more informed citizenry while helping municipalities become more efficient.


* 
**Long-Term**: Build a national, data-driven waste management network to support South Africa's climate goals.



## 👥 Team GreenDelta

* 
**Sabelo Mkhabela** - [64978451@mylife.unisa.ac.za](mailto:64978451@mylife.unisa.ac.za) 


* 
**Sthandiwe Mbokazi** - [22773886@mylife.unisa.ac.za](mailto:22773886@mylife.unisa.ac.za) 



## 🎥 Demo

Watch our project walkthrough on YouTube: [Eco Waste SA Demo](https://www.youtube.com/watch?v=jYIcFrTG5O8)
