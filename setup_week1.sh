#!/bin/bash

echo "Creating Week 1 documentation..."

mkdir -p docs

touch docs/project_proposal.md
touch docs/business_requirements.md
touch docs/business_rules.md
touch docs/data_dictionary.md
touch docs/kpi_definitions.md
touch docs/erd_design.md
touch docs/architecture.md

echo "# Supplier Quality Analytics Dashboard" > docs/project_proposal.md
echo "# Business Requirements" > docs/business_requirements.md
echo "# Business Rules" > docs/business_rules.md
echo "# Data Dictionary" > docs/data_dictionary.md
echo "# KPI Definitions" > docs/kpi_definitions.md
echo "# ERD Design" > docs/erd_design.md
echo "# System Architecture" > docs/architecture.md

git add .

git commit -m "Week 1 documentation structure"

git push origin main

echo ""
echo "Week 1 setup completed!"