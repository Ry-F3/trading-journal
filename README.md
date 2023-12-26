

# Trader Tribe 

# Code Institute Portfolio Project 4: Django Full-Stack Toolkit -  deployed via Github.
### To view the project please [click here](https://trader-tribe-7c9dc3cf075d.herokuapp.com/).
<br>

![Index page screenshot]()

## **Scope**

Trader Tribe is a specialised trading journal app meticulously crafted to meet the distinct requirements of traders within a niche market. The app offers users a dynamic platform to journal their trades with ease, equipped with robust tools for meticulous tracking of profits and losses. More than just a personal tracking tool, Trade Tribe cultivates a vibrant community space where users can share their unique trading experiences with fellow enthusiasts.

Key Features
1. **Dynamic Trade Journaling:**
Seamlessly record and document trade details, including symbols, dates, position sizes, margins, leverage, and more.
The dynamic row system ensures a personalised and organised trade journal tailored to each user.
2. **Profit and Loss Tracking:**
Real-time monitoring of profits and losses associated with each trade, providing valuable insights into overall portfolio performance.
3. **Community Engagement:**
Create a collaborative atmosphere where users can share insights, strategies, and the highs and lows of their trading journey.
Explore and learn from the experiences of other users within the Trader Tribe community.
4. **User-Friendly Interface:**
Intuitive and user-friendly design makes Trader Tribe accessible to traders of all levels of expertise.

## **Audience**

Trade Tribe caters to a diverse audience of traders seeking a comprehensive tool to enhance their trading experience. Our target audience includes traders from various backgrounds and styles, each with unique needs and preferences.

### **Types of Traders**

* Day Traders:
    * Description: Engage in buying and selling within the same day.
    * Characteristics: Quick decision-makers, monitor intraday charts, execute multiple trades.
    * Needs: Real-time market data, fast execution platforms, risk management tools.
* Swing Traders:
    * Description: Hold positions for days to weeks to capture price swings.
    * Characteristics: Analyse technical and fundamental factors, moderate trading frequency.
    * Needs: Charting tools, trend analysis, risk-reward calculators.
* Position Traders:
    * Description: Take a long-term investment approach, holding for weeks, months, or years.
    * Characteristics: Focus on fundamental analysis, less concerned with short-term fluctuations.
    * Needs: Fundamental data, macroeconomic indicators, portfolio management tools.
* Scalpers:
    * Description: Make numerous short-term trades to profit from small price movements.
    * Characteristics: Execute high-frequency trades, use technical indicators for entry and exit.
    * Needs: Low-latency trading platforms, real-time market data, low transaction costs.
* Algorithmic Traders:
    * Description: Use automated systems and algorithms for trading.
    * Characteristics: Develop and backtest algorithms, execute trades automatically.
    * Needs: Programming tools, historical market data, algorithm optimization features.
* Trend Followers:
    * Description: Capitalise on existing market trends.
    * Characteristics: Identify and ride momentum, use trend indicators.
    * Needs: Trend analysis tools, technical indicators, risk management features.
* Contrarian Traders:
    * Description: Take positions opposite to prevailing market sentiment.
    * Characteristics: Analyse sentiment indicators, go against the crowd.
    * Needs: Sentiment analysis tools, contrarian indicators, risk mitigation strategies.
* Event-Driven Traders:
    * Description: Base decisions on specific events impacting markets.
    * Characteristics: React to earnings reports, economic releases, geopolitical developments.
    * Needs: Economic calendars, news feeds, event-driven analysis tools.
* Options Traders:
    * Description: Trade options contracts for hedging or speculation.
    * Characteristics: Assess implied volatility, use various options strategies.
    * Needs: Options chain analysis, volatility calculators, options pricing models.
* Cryptocurrency Traders:
    * Description: Focus on trading cryptocurrencies.
    * Characteristics: Navigate volatile crypto markets, use technical analysis.
    * Needs: Cryptocurrency market data, blockchain analysis tools, secure wallets.

### **Bringing Traders Together: A Common Ground in Recording**
Regardless of their specific trading style—be it day trading, swing trading, position trading, or any other approach—serious traders share a common need: the ability to meticulously record and analyse their trades. Many exchanges have limitations on data retention, often erasing valuable trading history after a certain period.

Trade Tribe unifies this diverse community by providing a secure and reliable platform for traders to log their transactions comprehensively. Whether a day trader chasing intraday opportunities or a position trader taking a long-term investment approach, every trader benefits from a central repository that safeguards their trading data.
By offering categorization and filtering tools, Trade Tribe ensures that traders can effortlessly navigate through their trade history. This not only aids in performance analysis but also fosters a sense of confidence, knowing that their trading journey is documented and accessible whenever needed.

In essence, while trading styles and preferences may vary, the commitment to professional and meticulous record-keeping is the common thread that binds traders together within the Trade Tribe community.

## **User Stories**

### **Admin User Stories**

| **User Story**                         | **Acceptance Criteria**                                                                                                                                                                                                                                                                                                            |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| View All Trades:                       | - Admin should have access to a comprehensive list of all trades logged on the platform. - The list should display details such as user, trade ID, symbol, date, status, long/short, position, margin, leverage, open price, current price, and return/PnL.                                                                     |
| Filter Trades:                        | - Admin should be able to filter trades based on specific criteria, including user, date, symbol, and long/short. - The filtered results should provide a focused view for efficient analysis and management of trades.                                                                                                          |
| Search for Trades:                    | - Admin should be able to search for specific trades using keywords such as trading symbols or position sizes. - The search functionality should deliver quick and accurate results, enhancing the speed of locating and managing trades.                                                                                         |
| Associate Trades with Users:          | - Each trade should be associated with the correct user. - Admin should have a system to verify and ensure accurate user-specific trade records.                                                                                                               |
| Edit and Delete Trades:               | - Admin should have the ability to edit and delete trades when necessary. - The platform should facilitate easy corrections to ensure data accuracy.                                                                                                               |
| Manage User Permissions:              | - Admin should be able to manage user permissions related to trades. - This includes controlling which users can view, edit, or delete specific trades. - The permission management system should be robust and user-friendly.                                              |


### **Unregistered User Stories**

| **User Story**               | **Acceptance Criteria**                                                                                                                                                                                         |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sign Up for a New Account:   | - As an unregistered user, I want the ability to sign up for a new account on the Trade Tribe platform. - The sign-up process should include fields for username, email, and password. - Upon successful sign-up, the user should receive a confirmation message.                   |
| Explore Platform Features:   | - After signing up, the unregistered user should have the ability to explore the platform features without logging in. - This includes viewing informational pages, learning about the app's functionalities, and understanding the benefits of creating a trading journal. |
| Access Demo Trades:           | - Unregistered users should have access to a demo or sample trades section to understand how the trading journal works. - This allows users to explore the platform's capabilities before committing to creating a full account.                                                   |
| Learn About Community:        | - Provide information to unregistered users about the community aspect of Trade Tribe. - Showcase the benefits of joining the community, such as sharing trading experiences, gaining insights, and connecting with other traders.                               |
| Clear Call-to-Action:         | - Display a clear call-to-action for unregistered users to encourage them to sign up for an account. - The call-to-action should highlight the value proposition of creating a trading journal and participating in the Trade Tribe community.                             |


### **Registered User Stories**

| User Story                                                     | Description                                                                                                      |
|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| I want to be able to have my personal account                  | As a member of the Trade Tribe community, I want to create and manage my personal account, including profile customization, profile picture upload, and the ability to set privacy preferences. This ensures a personalised and secure experience on the platform. |
| I want to be able to log my trades                              | As a trader within the Trade Tribe app, I aim to log comprehensive details of each trade, including the trading symbol, date, position size, margin, leverage, open and current prices, return/loss, and additional notes to provide context for each trade. This detailed logging helps me analyse and learn from each trading decision. |
| I want to be able to filter my trades by various criteria       | As a Trade Tribe user, I should have the flexibility to filter my trades based on diverse criteria such as day, month, year, trading symbol, profit, loss, open trades, closed trades, and specific trading strategies. This enables me to conduct in-depth analysis and review my trading history based on specific parameters.|
| I want to be able to see my PnL                                | As a dedicated trader on Trade Tribe, I desire a visually intuitive display of my Profit and Loss (PnL) across all trades. The PnL summary should include performance metrics, visual charts, and the ability to track PnL over different time frames. This feature assists me in evaluating my overall trading performance and making informed decisions.|
| I want to be able to share my trade with the community           | Being a part of the Trade Tribe community, I aspire to share my trading experiences with fellow traders. The platform should facilitate easy sharing of trade details, including trade snapshots, charts, and insights. Additionally, the sharing feature should allow me to engage in discussions, seek advice, and provide valuable input to the community.      |
| I want to receive feedback on my trades                         | As a trader on Trade Tribe, I value constructive feedback from the community. I want the ability to receive comments, likes, and discussions on my shared trades. This interactive feedback loop enhances the learning experience and encourages collaboration within the community. |
| I want to track my trading performance over time               | To monitor my progress and growth as a trader, I need the ability to track and visualise my trading performance over different time periods. This includes performance analytics, historical data charts, and a performance summary dashboard to help me identify strengths and areas for improvement. |
| I want to set trading goals and receive notifications          | As a motivated trader, I want to set specific trading goals, such as weekly profit targets or risk limits. The app should allow me to input these goals and send notifications or reminders to help me stay focused and disciplined in achieving my objectives. |
| I want to discover new trading strategies from the community   | To expand my trading knowledge, I wish to explore and learn from the experiences of other traders. The platform should feature a discovery section where traders can share unique strategies, insights, and educational content. This encourages continuous learning and the exploration of diverse trading approaches. |
| I want to connect with traders who share similar interests     | Trade Tribe should offer a social feature that enables me to connect with traders who share similar trading styles, interests, or goals. This social networking aspect fosters a sense of community, allowing me to build connections, share experiences, and collaborate with like-minded traders. |
| I want to be able to export my trades to a PDF                   | As a Trade Tribe user, I want the ability to export my trade data to a PDF format. This feature enables me to create a portable and shareable document containing my trade details, facilitating easy record-keeping and analysis outside of the platform. |


## **Models**

### Trade database model

| Symbol | Date       | Status | L/S  | Risk | Margin | Leverage | Open Price | Closed Price | Return PnL |
|--------|------------|--------|------|------|--------|----------|------------|--------------|------------|
| AAPL   | 2023-01-01 | Open   | Long | 2%  | 1000   | 2x       | $150       | $160         | $100       |
| GOOGL  | 2023-01-02 | Closed | Short| 4% | 2000   | 1.5x     | $200       | $180         | -$300      |
| MSFT   | 2023-01-03 | Open   | Long | 2.5%  | 1500   | 2.5x     | $120       | $130         | $75        |

<br>

![Trade database model](/readme/images/trade-database-model.png)

<br>

How does user data get stored?:
* User-Centric Rows: The system employs a dynamic row system, where each user maintains their unique set of rows. For example:
* User ID = A has rows [1, 2, 3, 4, 5]
* User ID = B has rows [1, 2, 3, 4]
* User ID = C has rows [1, 2, 3, 4, 5]

This dynamic row structure ensures a personalised and organized record-keeping system for each user, facilitating easy management and retrieval of trade information, without database conflictions.




## **Wireframes**


## **Layout**


## **Features**

### **Navbar** 

### **Future Enhancements:**


## **Favicon** 


### **Unified colour scheme**

### **Accessibility**


## **Bugs**

**List of known bugs:**


**List of fixed bugs**


## **Technologies**

## **Testing**

### **Testing User Stories**


### **Testing functionality**


### **Deployment**



### **Testing on different devices**


### **Testing code**


#### **JavaScript Validation**  using *[jshint](https://jshint.com/)* :
 

#### **CSS validation** using [jigsaw](https://jigsaw.w3.org/css-validator/validator) :



#### **Lighthouse performance testing**


## **Credits**

Developed by **Rhys.Alexander.Few**

### **Code**

**Peer Review**


**Other Resources**


**Bibliography:**










