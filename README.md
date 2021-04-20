# Stock-Market-Similation

Caution: These tools are written by me and I used them for a small period of time to test an automatized strategy of stockmarket trading. Unfortunately, I didn't write any 
documantation for these tools so probably no one will really use them. But still I want to keep them here.


These tools simulate buy and sells according to some parameters that are set to describe a trade strategy using MACD inducator. Simulation uses stock prices data in csv format. Simulation divides the data into smaller parts and inspects them separately to prevents biosed results. After simulation runs,
performance of the strategy is descriebed by writing some important parameters (like mean, std of gains and loses) on console and drawing useful graphs (like histagrom of gains and loses, prices of stock and 
buying selling points). I added a screenshot of graphs that main.py draws: sample_image.png.

+ graphs are drawn using matplotlib.
+ macd inducator's values are calculated using a library called ta.
+ Data is processed using Pandas.


