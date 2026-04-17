# Simple Python Blog Generator Template
# Generates when run Html page with required content on it. I preferred using this to local template.
# Blog is hosted when file is run and can be accessed locally

import os
from datetime import datetime

# Folder structure with Outer Page with post on it
OUTPUT_DIR = "site"
POSTS_DIR = "posts"

# Basic HTML template - written for me in AI
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .date {{ color: gray; font-size: 0.9em; }}
        .content {{ margin-top: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="date">{date}</div>
    <div class="content">
        {content}
    </div>
    <hr>
    <a href="index.html">← Back to Home</a>
</body>
</html>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>My Blog</title>
</head>
<body>
    <h1>My Blog</h1>
    <ul>
        {posts}
    </ul>
</body>
</html>
"""

# Writing post, with title, date,n name and content (including visualisations built)
posts = [
    {
        "title": "How is the UKs energy provision changing over time?",
        "date": "2026-04-14",
        "filename": "blog-uk-energy.html",
        "content": """
<h2>Introduction</h2>

<p>Recently, due to rapidly accelerating global affairs, increasing climate pressures, and perhaps simply reaching adulthood, I have become increasingly aware of energy use in everyday life. Whether filling up my car at a petrol station or plugging in an electric vehicle to charge, I question: will there be enough petrol for me to get home? Will I be stranded? Will I wake up in the morning with an uncharged phone? Will all power fail suddenly overnight?</p>

<p>I, like many others, have grown up in a world where leaving lights on, charging devices overnight, or turning up the heating comes without much thought. However, I have come to realise that this level of energy security is a privilege. These increasing concerns motivated this project: to better understand how the UK produces energy and the extent to which it relies on overseas provision—something I had not previously considered in depth.</p>

<p>One inspiration behind this project was Kate Morley, whose website I later reference in relation to my web scraping work. I was also encouraged by my father, who has a strong interest in energy systems and first introduced me to this topic. I also have an interest in whether or not we are adjusting and adapting ovetime to overcome economic and environmental challenges which will be explored later.</p>

<p>After exploring annual, monthly, and daily data, my findings suggest that the UK is moving away from coal as a source of energy provision and transitioning towards renewables—particularly wind and nuclear generation, while becoming less dependent on overseas provision.</p>


<h2>Past Few Decades of Electricity Generation</h2>

<img src="../Visualisations/annual-renewable-generation.gif" alt="Annual Renewable Generation Trends" style="width:100%; margin-top:20px; border-radius:10px;">

<p>The graph above illustrates the growth of renewable energy generation in the UK since 1996. Wind power generation (both offshore and onshore) began to increase significantly in the early 2000s, while solar energy contributed a much smaller share of generation, only generating noticable amounts of power in the last 15 years.</p>

<p>This graph raises several key questions:</p>
<ul>
    <li><a href="#wind-vs-solar">Why is wind growing faster than solar?</a></li>
    <li><a href="#wind-growth">How fast is wind generation increasing?</a></li>
    <li><a href="#non-renewables">What about non-renewable energy generation?</a></li>
    <li><a href="#energy-mix">What does the current energy mix look like?</a></li>
</ul>

<p>Let’s tackle these questions one at a time.</p>


<h3 id="wind-vs-solar">Why is wind growing faster than solar?</h3>

<p>In the graph below, monthly renewable energy generation for Major Power Producers (MPPs) is shown:</p>

<img src="../Visualisations/monthly-mpps-renewable-generation.gif" alt="Monthly Renewable Generation Trends" style="width:100%; margin-top:20px; border-radius:10px;">

<p>Clear seasonal trends can be observed from solar generation, with a smooth oscillating pattern—higher production in summer months and lower in winter—becoming visible from around 2014. Despite this, solar output remains significantly lower than wind.</p>

<p>One explanation for this disparity is efficiency and consistency. A wind turbine can approximately produce 
<a href="https://www.compareyourfootprint.com/wind-vs-solar-green-energy-winning/" target="_blank">forty-eight thousand times the amount of energy per kWh</a>, 
than a solar panel can. Additionally, solar panels are limited to daylight hours, whereas wind (particularly offshore) can generate electricity more consistently, due to relatively constant wind.</p>

<p>These factors help explain the faster growth of wind power generation, although solar remains an attractive option for domestic energy generation.</p>


<h3 id="wind-growth">How fast is wind generation increasing?</h3>

<p>Between January 2007 and 2026, wind generation increased by approximately 9.25 terawatt hours (TWh) on a monthly basis, as shown below.</p>

<div style="margin-top:20px;">
    <iframe src="../Visualisations/monthly-wind-generation.html" width="100%" height="500px" style="border:none; border-radius:10px;"></iframe>
</div>

<p>Recent trends highlight rapid growth, although not in this dataset, according to 
<a href="https://www.reuters.com/business/energy/record-wind-output-helps-shield-uk-worst-iran-war-fallout-2026-03-31/" target="_blank">Reuters</a>, 
wind output surged by 33% between January and March 2026 compared to the same period in 2025.</p>

<p>Large offshore wind projects have contributed significantly to this growth. For example, Hornsea became the largest offshore wind farm in the world in 2022, with 339 turbines, as highlighted in 
<a href="https://www.businessenergydeals.co.uk/blog/wind-farms-in-the-uk/" target="_blank"> this overview of UK wind farms</a>.

<p>With the growth in wind power capacity, electricitygeneration records continue to be set. On 25 March 2026, the UK generated 23,880 MW of wind power within a half-hour period 
(<a href="https://renewablesnow.com/news/great-britain-sets-new-wind-generation-record-1292116/" target="_blank">Renewables Now</a>).</p>

<p>This sustained growth highlights the UK’s increasing reliance on wind as a core component of energy provision and is likely to have helped mitigate impacts from global conflicts and we can only hope that it will continue to do so.</p>


<h3 id="non-renewables">What about non-renewable energy generation in the UK?</h3>

<p>The pie charts below show the average fuel mix used in UK electricity generation across each time period.</p>

<div style="margin-top:20px;">
    <iframe src="../Visualisations/combined_energy_pie_charts.html" width="100%" height="500px" style="border:none; border-radius:10px;"></iframe>
</div>
<p><small>[Hover over chart to reveal more information]</small></p>

<p>Over the past two decades, there has been a clear shift away from coal. Between 2000–2005, coal accounted for 33.36% of energy generation. By 2020–2024, this had fallen to just 1.59%, despite the marginal increase in coal use in 2010-2014. Also the output from Nuclear (a renewable fuel) has fallen in the last 20 years.</p>

<p>Meanwhile, renewable sources—particularly wind, solar, and biomass—have expanded significantly. 
<a href="https://www.reuters.com/business/energy/record-wind-output-helps-shield-uk-worst-iran-war-fallout-2026-03-31/" target="_blank">
Biomass generation</a>.
has also reached record levels of output recently, which has helped lift the UK's renewable output share.</p>

<p>Gas, however, is still extensively used in energy production. As a non-renewable fuel, this reliance exposes the UK to geopolitical risks such as the conflict in Iran, which has pushed up current prices on oil and natural gas. </p>
<p>Fortunately, oil contributes to only a small proportion of UK electricity generation (around 0.66% between 2020–2024), although it remains critical as a transport fuel.</p>


<h2>Trade</h2>

<h3>Are we becoming less reliant on overseas energy provision over time?</h3>

<p>Something that had never occurred to me before beginning this project was what happened to the excess energy we produce? Or an even more pressing issue of what happens if we don’t produce enough energy? In reality, international energy transfers play a crucial role.</p>

<img src="../Visualisations/trade-balance-animation.gif" alt="Energy Trade" style="width:100%; margin-top:20px; border-radius:10px;">

<p>The animation above shows electricity imports and exports between the UK and neighbouring countries since 2017. While the UK imports fuels such as LNG and oil from nations across the globe, electricity trade is largely limited to geographically close countries due to infrastructure and efficiency constraints. Therefore, the UK recieves transfers mainly from European countries, with which it has undersea interconnectors for power trading.</p>

<p>The UK has consistently imported electricity from France (2017-2024). One reason for this is because France generates around 70% of its electricity from nuclear power
(<a href="https://mactech.co.uk/why-britains-nuclear-future-runs-through-france/" target="_blank">Britains nuclear future</a>), 
providing a stable and reliable supply that it can cheaply export to the UK.</p>

<p>Looking ahead, the planned 
<a href="https://www.nao.org.uk/work-in-progress/sizewell-c/" target="_blank">Sizewell C</a> nuclear power station built in the UK along the Suffolk coast is expected to generate 3.2 GWs annually (currently around 7% of UK demand) by the mid-2030s, when it becomes operational
This should help to reduce reliance on France and (increasingly) Norway for electricity.</p>

<p>Throughout this animation, except in 2022 the UK is in a trade deficit. In 2022, for the first time in 40 years the UK became a net exporter of electricity.
<a href="https://reports.electricinsights.co.uk/?p=1740" target="_blank">European energy crisis</a>
<p>This was largely due to nuclear outages (corrosion and cracking in reactor cores that required urgent maintenance) in France. Also the Russian invasion of Ukraine in 2022 meant that the EU lost a significant source of natural gas allowing the UK to plug the market, with  UK gas exports to the EU were over five times higher in summer 2022 than summer 2021 
(<a href=" https://www.energy-uk.org.uk/insights/the-power-of-partnership-uk-eu-energy-cooperation-for-a-clean-secure-future/" target="_blank">Energy Insights</a>).</p>

<p>Although recent trends suggest declining imports, this does not account for oil used in transport, which remains heavily import-dependent.</p>


<h2>Energy Used in Transport</h2>

<div style="margin-top:20px;">
    <iframe src="../Visualisations/fuel-consumption-line.html" width="100%" height="500px" style="border:none; border-radius:10px;"></iframe>
</div>
<p><small>[Hover over chart to reveal more information]</small></p>

<p>The graph above shows that, aside from the exception of 2020 due to COVID-19, transport fuel consumption has generally increased since 1970.</p>

<p>According to the 
<a href="https://www.gov.uk/government/statistics/national-travel-survey-2024/nts-2024-household-car-availability-and-trends-in-car-trips" target="_blank">UK National Travel Survey (2024)</a>, 
around 59% of households own petrol and 30% own diesel vehicles in the UK. This highlights the UK’s continued reliance on oil.</p>

<p>This dependence exposes the UK to global price shocks. For example, recent geopolitical tensions have led to fuel price increases, with petrol rising by 25p per litre and diesel by 48p 
(<a href="https://www.bbc.co.uk/news/articles/cvgk3qgkz41o" target="_blank">BBC News</a>).</p>

<p>However, there are signs of positive movement. Transport fuel consumption appears to have peaked around 2007 at 38.37 million tonnes and has since declined. Rising popularity of electric vehicles, combined with cleaner electricity generation, offers a pathway towards UK energy provision independence.</p>


<h2>Today’s Energy Provision (UK)</h2>

<h3 id="energy-mix">What does our energy generation mix look like today?</h3>

<p>After analysing annual and monthly generation trends, it is interesting to examine energy provision on a daily basis.</p>

<p>The image below shows today’s energy generation mix, total demand, and net transfers (imports & exports). This data is scraped from 
<a href="https://grid.iamkate.com/" target="_blank">grid.iamkate.com</a>.</p>

<div style="margin-top:20px;">
    <iframe src="../Visualisations/scraped-generation-mix.html" width="100%" height="500px" style="border:none; border-radius:10px;"></iframe>
</div>

<p><small>Data sourced from grid.iamkate.com by Kate Morley. Contains BMRS data © Elexon Limited (2026) and data from the National Energy System Operator and Carbon Intensity API.</small></p>
<p><small>[Hover over chart to reveal more information]</small></p>

<p>To update this daily view, run the web scraping script before generating the blog.</p>


<h2>Conclusion</h2>

<p>Renewable energy generation in the UK has expanded rapidly since around 2010, with wind playing a central role in day-to-day electricity supply in the UK. The continued development of infrastructure, such as offshore-wind farms and nuclear power stations (Sizewell C), offer the potential to further reduce reliance on fossil fuels and energy imports.</p>

<p>However, challenges remain—particularly the UK’s dependence on gas for electricity generation and oil for transport. These dependencies leave the country exposed to geopolitical and economic shocks.</p>

<p>With ongoing technological advancements and policy shifts, we can only hope for the transition towards a more sustainable and stable energy system in the UK.</p>

<p>I hope this project has also encouraged a more mindful approach to personal energy use—something increasingly relevant in today’s world.</p> """
    }
]

#Function for creating the blog and merging template with required ontent
def generate_post(post):
    html = BASE_HTML.format(
        title=post["title"],
        date=post["date"],
        content=post["content"]
    )

    filepath = os.path.join(OUTPUT_DIR, post["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html) #Saving to html


def generate_index(posts): #Doing the same for the index page.
    items = ""
    for post in posts:
        items += f'<li><a href="{post["filename"]}">{post["title"]}</a> ({post["date"]})</li>'

    html = INDEX_HTML.format(posts=items)

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for post in posts:
        generate_post(post)

    generate_index(posts)

    print("Blog generated! Open 'site/index.html' in your browser.")


if __name__ == "__main__":
    main()
#Completed blog page with visualisations