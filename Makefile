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
BLOG_OUT = site/blog-uk-energy.html

# Default
all: $(BLOG_OUT)

# --- Electricity (multiple outputs from one script) ---
$(ELECTRICITY_OUTPUTS):  python/electricity-generated.py
	$(PYTHON)  python/electricity-generated.py

# --- Other scripts ---
$(TRADE_OUT): python/trade-balance.py
	$(PYTHON) $<

$(FUEL_OUT): python/fuel-usage.py
	$(PYTHON) $<

$(SCRAPE_OUT): python/web-scrape.py
	$(PYTHON) $<

# --- Blog depends on everything ---
$(BLOG_OUT): python/blog.py $(ELECTRICITY_OUTPUTS) $(TRADE_OUT) $(FUEL_OUT) $(SCRAPE_OUT)
	$(PYTHON) python/blog.py

# --- Clean ---
clean:
	rm -f $(ELECTRICITY_OUTPUTS) $(TRADE_OUT) $(FUEL_OUT) $(SCRAPE_OUT) $(BLOG_OUT)