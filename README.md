# QUARNA - G-Quadruplex Analysis Tool

QUARNA is a web-based tool for analyzing G-Quadruplex structures in RNA/DNA. It provides comprehensive analysis for different types of G-Quadruplex formations including cyclic, linear, semi-cyclic, and star configurations.

## Features

- Analysis of multiple G-Quadruplex configurations:
  - Cyclic
  - Linear
  - Semi-cyclic
  - Star
- Support for different data sources:
  - HDRNA
  - NDB (Nucleic Acid Database)
  - NMR structures
  - X-RAY crystallography data
- Interactive 3D visualization using JSmol
- Downloadable results
- Comprehensive help documentation

## Project Structure

```
├── config/           # Django project configuration
├── dataset/          # Structural datasets by configuration type
│   ├── cyclic/
│   ├── linear/
│   ├── semi_cyclic/
│   └── star/
├── media/           # User uploaded files and results
├── quartet_finder/  # Main Django application
├── scripts/        # Analysis scripts for different configurations
│   ├── bpfind/    # Base-pair finding tools
│   ├── cyclic/
│   ├── linear/
│   ├── quad_scripts/
│   ├── semi_cyclic/
│   └── star/
├── static/         # Static assets (CSS, JS, images)
└── templates/      # HTML templates
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd QUARNA
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create static files:
```bash
python manage.py collectstatic
```

## Usage

1. Start the development server:
```bash
python manage.py runserver
```

2. Visit http://localhost:8000 in your web browser

## Data Sources

The tool uses structural data from various sources:
- HDRNA (High Definition RNA Database)
- NDB (Nucleic Acid Database)
- NMR structures
- X-RAY crystallography data

Each type of G-Quadruplex configuration (cyclic, linear, semi-cyclic, star) has its own dataset collection in these categories.

## Tools

- **BPFind**: Base-pair finding tool (version 1.83)
- Configuration-specific analysis scripts for:
  - Cyclic structures
  - Linear structures
  - Semi-cyclic structures
  - Star formations
- Specific residue analysis tools

## License

[Add license information]

## Contributors

[Add contributor information]

## Acknowledgments

- IIIT (International Institute of Information Technology)
