
{
    # Module information
    "name": "Custom Report",
    "version": "14.0.1.0.0",
    "category": "Sales Management",
    "sequence": "1",
    "summary": """Reportes con imagenes de productos y categoria.""",
    "description": """Reportes con imagenes de productos y categoria.""",
    "license": "LGPL-3",
    # Author
    "author": "Xavier Méndez",
    "website": "https://www.freelancer.com/u/novadragonsoftwa",
    "maintainer": "Xavier Méndez",
    # Dependencies
    "depends": ["sale_management"],
    # Views
    "data": ["views/sale_product_view.xml", "views/report_saleorder.xml"],
    "installable": True,
    "auto_install": False,
}
