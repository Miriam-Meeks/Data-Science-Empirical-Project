PYTHON = python3

# Electricity outputs
ELECTRICITY_OUTPUTS = \
	Visualisations/combined_energy_pie_charts.html \
	Visualisations/annual-renewable-generation.gif \
	Visualisations/monthly-mpps-renewable-generation.gif \
	Visualisations/monthly-wind-generation.html

# Other outputs (adjust as needed)
TRADE_OUT = Visualisations/trade-balance-animation.gif
FUEL_OUT  = Visualisations/fuel-consumption-line.html
SCRAPE_OUT = Visualisations/scraped-generation-mix.html
BLOG_OUT = blog-uk-energy.html

# Default
all: $(BLOG_OUT)

# --- Electricity (multiple outputs from one script) ---
$(ELECTRICITY_OUTPUTS): electricity-generated.py
	$(PYTHON) electricity-generated.py

# --- Other scripts ---
$(TRADE_OUT): trade-balance.py
	$(PYTHON) $<

$(FUEL_OUT): fuel-usage.py
	$(PYTHON) $<

$(SCRAPE_OUT): web-scrape.py
	$(PYTHON) $<

# --- Blog depends on everything ---
$(BLOG_OUT): blog.py $(ELECTRICITY_OUTPUTS) $(TRADE_OUT) $(FUEL_OUT) $(SCRAPE_OUT)
	$(PYTHON) blog.py

# --- Clean ---
clean:
	rm -f $(ELECTRICITY_OUTPUTS) $(TRADE_OUT) $(FUEL_OUT) $(SCRAPE_OUT) $(BLOG_OUT)