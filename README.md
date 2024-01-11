

# Trader Tribe 

# Code Institute Portfolio Project 4: Django Full-Stack Toolkit -  deployed via Github.
### To view the project please [click here](https://trader-tribe-7c9dc3cf075d.herokuapp.com/).
<br>

![Index page screenshot]()

## **Scope**

Trader Tribe is a specialised trading journal app meticulously crafted to meet the distinct requirements of traders within a niche market. The app offers users a dynamic platform to journal their trades with ease, equipped with robust tools for meticulous tracking of profits and losses. More than just a personal tracking tool, Trader Tribe cultivates a vibrant community space where users can share their unique trading experiences with fellow enthusiasts.

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

Trader Tribe caters to a diverse audience of traders seeking a comprehensive tool to enhance their trading experience. Our target audience includes traders from various backgrounds and styles, each with unique needs and preferences.

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

Trader Tribe unifies this diverse community by providing a secure and reliable platform for traders to log their transactions comprehensively. Whether a day trader chasing intraday opportunities or a position trader taking a long-term investment approach, every trader benefits from a central repository that safeguards their trading data.
By offering categorization and filtering tools, Trader Tribe ensures that traders can effortlessly navigate through their trade history. This not only aids in performance analysis but also fosters a sense of confidence, knowing that their trading journey is documented and accessible whenever needed.

In essence, while trading styles and preferences may vary, the commitment to professional and meticulous record-keeping is the common thread that binds traders together within the Trader Tribe community.

## **User Stories**

### **Admin User Stories**

| **User Story**                         | **Acceptance Criteria**                                                                                                                                                                                                                                                                                                            |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| View All Trades:                       | Admin should have access to a comprehensive list of all trades logged on the platform. The list should display details such as user, trade ID, symbol, date, status, long/short, position, margin, leverage, open price, current price, and return/PnL.                                                                     |
| Filter Trades:                        | Admin should be able to filter trades based on specific criteria, including user, date, symbol, and long/short. The filtered results should provide a focused view for efficient analysis and management of trades.                                                                                                          |
| Search for Trades:                    | Admin should be able to search for specific trades using keywords such as trading symbols or position sizes. The search functionality should deliver quick and accurate results, enhancing the speed of locating and managing trades.                                                                                         |
| Associate Trades with Users:          | Each trade should be associated with the correct user. Admin should have a system to verify and ensure accurate user-specific trade records.                                                                                                               |
| Edit and Delete Trades:               | Admin should have the ability to edit and delete trades when necessary. The platform should facilitate easy corrections to ensure data accuracy.                                                                                                               |
| Manage User Permissions:              | Admin should be able to manage user permissions related to trades. This includes controlling which users can view, edit, or delete specific trades. The permission management system should be robust and user-friendly.                                              |


### **Unregistered User Stories**

| **User Story**               | **Acceptance Criteria**                                                                                                                                                                                         |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sign Up for a New Account:   | As an unregistered user, I want the ability to sign up for a new account on the Trader Tribe platform. The sign-up process should include fields for username, email, and password. Upon successful sign-up, the user should receive a confirmation message.                   |
| Explore Platform Features:   | After signing up, the unregistered user should have the ability to explore the platform features without logging in. This includes viewing informational pages, learning about the app's functionalities, and understanding the benefits of creating a trading journal. |
| Access Demo Trades:           | Unregistered users should have access to a demo or sample trades section to understand how the trading journal works. This allows users to explore the platform's capabilities before committing to creating a full account.                                                   |
| Learn About Community:        | Provide information to unregistered users about the community aspect of Trader Tribe. Showcase the benefits of joining the community, such as sharing trading experiences, gaining insights, and connecting with other traders.                               |
| Clear Call-to-Action:         | Display a clear call-to-action for unregistered users to encourage them to sign up for an account. The call-to-action should highlight the value proposition of creating a trading journal and participating in the Trader Tribe community.                             |


### **Registered User Stories**

| **User Story**                                                     | **Acceptance Criteria**                                                                                                      |
|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| I want to be able to have my personal account                  | As a member of the Trader Tribe community, I want to create and manage my personal account, including profile customization, profile picture upload, and the ability to set privacy preferences. This ensures a personalised and secure experience on the platform. |
| I want to be able to log my trades                              | As a trader within the Trader Tribe app, I aim to log comprehensive details of each trade, including the trading symbol, date, position size, margin, leverage, open and current prices, return/loss, and additional notes to provide context for each trade. This detailed logging helps me analyse and learn from each trading decision. |
| I want to be able to filter my trades by various criteria       | As a Trader Tribe user, I should have the flexibility to filter my trades based on diverse criteria such as day, month, year, trading symbol, profit, loss, open trades, closed trades, and specific trading strategies. This enables me to conduct in-depth analysis and review my trading history based on specific parameters.|
| I want to be able to see my PnL                                | As a dedicated trader on Trader Tribe, I desire a visually intuitive display of my Profit and Loss (PnL) across all trades. The PnL summary should include performance metrics, visual charts, and the ability to track PnL over different time frames. This feature assists me in evaluating my overall trading performance and making informed decisions.|
| I want to be able to share my trade with the community           | Being a part of the Trader Tribe community, I aspire to share my trading experiences with fellow traders. The platform should facilitate easy sharing of trade details, including trade snapshots, charts, and insights. Additionally, the sharing feature should allow me to engage in discussions, seek advice, and provide valuable input to the community.      |
| I want to receive feedback on my trades                         | As a trader on Trader Tribe, I value constructive feedback from the community. I want the ability to receive comments, likes, and discussions on my shared trades. This interactive feedback loop enhances the learning experience and encourages collaboration within the community. |
| I want to track my trading performance over time               | To monitor my progress and growth as a trader, I need the ability to track and visualise my trading performance over different time periods. This includes performance analytics, historical data charts, and a performance summary dashboard to help me identify strengths and areas for improvement. |
| I want to set trading goals and receive notifications          | As a motivated trader, I want to set specific trading goals, such as weekly profit targets or risk limits. The app should allow me to input these goals and send notifications or reminders to help me stay focused and disciplined in achieving my objectives. |
| I want to discover new trading strategies from the community   | To expand my trading knowledge, I wish to explore and learn from the experiences of other traders. The platform should feature a discovery section where traders can share unique strategies, insights, and educational content. This encourages continuous learning and the exploration of diverse trading approaches. |
| I want to connect with traders who share similar interests     | Trader Tribe should offer a social feature that enables me to connect with traders who share similar trading styles, interests, or goals. This social networking aspect fosters a sense of community, allowing me to build connections, share experiences, and collaborate with like-minded traders. |
| I want to be able to export my trades to a PDF                   | As a Trader Tribe user, I want the ability to export my trade data to a PDF format. This feature enables me to create a portable and shareable document containing my trade details, facilitating easy record-keeping and analysis outside of the platform. |


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

## **ElephantSQL for Database Hosting:**

Trader Tribe uses ElephantSQL as the database hosting provider. ElephantSQL is a Database as a Service (DBaaS) platform that specializes in providing managed PostgreSQL databases in the cloud. PostgreSQL is a powerful, open-source relational database management system (RDBMS) known for its extensibility and support for advanced data types.

**Key Points:**

* Managed PostgreSQL Database: ElephantSQL takes care of managing the PostgreSQL database, handling tasks such as backups, updates, and scaling. This allows Trader Tribe developers to focus on building and improving the application rather than managing database infrastructure.

* Cloud-Based Service: ElephantSQL operates in the cloud, providing a scalable and reliable environment for hosting databases. This ensures that Trader Tribe's database can grow with the increasing number of users and data.

* Ease of Use: ElephantSQL offers a user-friendly interface for managing PostgreSQL databases. It simplifies database administration tasks, making it accessible for developers of varying skill levels.

* Security: ElephantSQL implements security measures to protect databases, including encryption for data in transit and at rest. This is crucial for ensuring the confidentiality and integrity of user data in Trader Tribe.

* Integration with Django: ElephantSQL seamlessly integrates with Django, the web framework used for developing Trader Tribe. Django's ORM (Object-Relational Mapping) simplifies the interaction with the database, allowing developers to work with database entities using Python code.

**User Stored Data:**
* User-Centric Rows: The system employs a dynamic row system, where each user maintains their unique set of rows. For example:
* User ID = A has rows [1, 2, 3, 4, 5]
* User ID = B has rows [1, 2, 3, 4]
* User ID = C has rows [1, 2, 3, 4, 5]

This dynamic row structure ensures a personalised and organized record-keeping system for each user, facilitating easy management and retrieval of trade information, without database conflictions.

## **Wireframes**

![sign-in](/readme/wireframes/wireframe-sign-in.png)

<br>

![sign-home](/readme/wireframes/wireframe-home.png)

<br>

![sign-trades](/readme/wireframes/wireframe-trades.png)

<br>

![sign-contact](/readme/wireframes/wireframe-contact.png)

<br>

![sign-blog](/readme/wireframes/wireframe-blog.png)

## **Layout**


## **Features**

![Home-dashboard](/readme/screenshots/home-dashboard.png)

### **Home Dashboard Overview:**

#### **Files used:**
* Front end Javascript/jQuery: chart.js, currencySwap.js, editButton.js, formFunction.js, global.js, longShort.js
* Backend (Django): views.py, urls.py, models.py, forms.py

1. Diverse Toolset:
    * Empower users with a comprehensive range of tools for effective trade management. The dashboard is designed to provide users with a versatile toolkit, catering to various aspects of trade analysis and record-keeping.
2. Alpha Mockup Stage:
    * The current stage of development is the alpha mockup, acknowledging that there are features yet to be implemented. Due to time constraints, some functionalities were left out. The dashboard serves as a foundation for future enhancements and refinements.
3. Progress Tracking with Matplotlib:
    * For ease of learning, the dashboard incorporates the matplotlib.pyplot package to offer users a visual representation of their progress. Interactive chart investigation remains a potential avenue for future development.
4. Trade Summaries in PDF:
    * Users have the capability to generate PDF summaries of their trades. This feature provides a convenient way to document and review trade activities.
5. Dynamic Trade Recording:
    * Enable users to dynamically record trades by creating, saving, editing, and deleting entries. This flexibility ensures efficient management of trade data.
6. Realised and Unrealized Profit Tracking:
    * The Profit and Loss (PnL) feature updates in real-time, reflecting both realised and unrealized profits. This dynamic display is dependent on the status of each trade (open or closed).
7. Portfolio Balance Updates:
    * Users can update their portfolio balance, and the system automatically adjusts it based on closed trades. This ensures an accurate and up-to-date reflection of the user's financial standing.
8. Trade Search Functionality:
    * The dashboard includes a side-bar with filters, allowing users to easily search and filter trades. This feature streamlines the process of locating specific trade records.
9. Call to Action for Trade Journaling:
    * Encourage users to start journaling their trades through a prominent call to action. This guides users to the relevant section of the dashboard for accessing and maintaining their trade journals.
The dashboard, although in the alpha mockup stage, lays the groundwork for a feature-rich platform with a focus on user-friendly trade management and analysis.

### **Generate PDF Report**

![Home-dashboard-trade-report](/readme/screenshots/home-dashboard-trade-report.png)

#### **Implementation Details**

1. Import Necessary Modules into views.py: <br> <code> from reportlab.lib.pagesizes import letter
from reportlab.pdfgen <br> import canvas
from io import BytesIO </code>

2. Define the <code>generate_pdf_report</code> Function: <br> This function takes a user object and a queryset of trades as input and generates a PDF report with trade details. It uses ReportLab's canvas module to create a PDF document.

3. Usage in <code>generate_report</code> View Function: <br> In the generate_report view function, when the user selects the PDF format, it calls generate_pdf_report to create the PDF content. The generated PDF is then sent as an HTTP response for the user to download. The code for future iterations has been left to show how more file types could be called by the user i.e CSV files.

### **Create Trade**

![Home-dashboard-create-trade](/readme/screenshots/home-dashboard-create-trade.png)


#### **Implementation Details**

1. Frontend (JavaScript/jQuery):
    * The functionality starts with a button or element with the id showCreateTradeForm. This element is used to trigger the visibility of the form for creating a new trade.
The function is wrapped in $(document).ready(), ensuring that it executes once the document is fully loaded.
The form elements and related components are selected using jQuery, such as createTradeForm, showCreateTradeForm, hideCells, and container.
A flag createTradeFormActive is used to track whether the form is currently active or not.

2. Event Listeners:
    * The "Create Trade" button click is captured using showCreateTradeForm.click(function () {...}). Depending on the current state, it either displays or hides the trade creation form.
Inside the click event handler, the text of the button is checked. If it's "Create Trade," it shows the form; if it's "Cancel Trade," it hides the form.

3. Form Visibility Handling:
    * The handleFormVisibility function is defined to manage the visibility and behavior of the form.
If the form is active (createTradeFormActive is true), it adjusts the styling and behavior for an active form. It clears form fields, hides specific cells, and disables certain input fields.
If the form is inactive, it resets the styling and behavior for an inactive form, scrolls to the top of the container, and clears form fields.

4. Save Type and Button Text:
    * The function sets the value of a hidden input field with the id saveType based on whether the form is active or not.
It toggles the CSS classes of the "Save" button based on the form's activity, changing the button's appearance.

5. Input Field Handling:
    * The function handles the enabling and disabling of input fields based on the form's activity.
It sets the value of saveType to 'regular' if the form is active and 'overwrite' if the form is inactive.

6. Reverting Button Text:
    * The text of the button is reverted based on the form's activity. If the form is active, the button text becomes "Cancel Trade"; if inactive, it becomes "Create Trade."

7. Backend (Django):
    * In Django, there are views (HomeView and update_portfolio_balance, among others) that handle the backend logic when a trade is created or canceled.
The Trade model is used to store trade-related data, and there are functions to calculate and update the portfolio balance and realized profits.
Usage:

The functionality is used within Django templates to create and cancel trades. It interacts with Django views to handle the backend logic and updates.


### **Long and Short Calculations**

#### **As seen in file global.js & longShort.js :**

1. Long Position Calculation (performLongCalculations()):
* Input Parameters:
    * leverage: The leverage used for the trade.
    * margin: The margin allocated for the trade.
    * openPrice: The initial price at which the position was opened.
    * currentPrice: The current market price.
* Steps:
    * Calculate the percentage change in the asset's price:<br> <code> // Calculate percentage Long Change <br> var percentageLongChange = ((currentPrice - openPrice) / openPrice) * leverage * 100; </code>
    * Format the percentage change to two decimal places.
    * Calculate the return PnL (Profit and Loss): <br><code> // Calculate Return PnL for Long Position <br> var returnPnlLong = (100 / percentageLongChange) * margin; </code>
    * Update the HTML element with the id 'id_return_pnl' with the calculated return PnL value.

2. Short Position Calculation (performShortCalculations()):
* Input Parameters:
    * leverage: The leverage used for the trade.
    * margin: The margin allocated for the trade.
    * openPrice: The initial price at which the short position was opened.
    * currentPrice: The current market price.
* Steps:
    * Calculate the percentage change in the asset's price for a short position: <code> // Calculate percentage Short Change <br> var percentageShortChange = ((openPrice - currentPrice) / openPrice) * leverage * 100; </code>
    * Format the percentage change to two decimal places.
    * Calculate the return PnL (Profit and Loss): <br><code> // Calculate Return PnL for Short Position <br> var returnPnlShort = (100 / percentageShortChange) * margin; </code>
    * Update the HTML element with the id 'id_return_pnl' with the calculated return PnL value.


### **Edit Trade**

![Home-dashboard-edit-trade](/readme/screenshots/home-dashboard-edit-trade.png)




### **Trading Journal**

jQuery was selected to craft a fully functional trading journal with an interactive and user-friendly interface. The vision was to ensure a seamless development process, elevate code readability, and enrich the user experience by leveraging jQuery's robust utilities for DOM manipulation, event handling, and AJAX communication. This choice proved especially valuable in constructing dynamic web applications, where real-time updates and user interactions are pivotal components of the overall experience.

**Key points on why jQuery best served the task at hand:**

* **DOM Manipulation:**
    * jQuery simplifies DOM manipulation, making it easier to select, traverse, and manipulate HTML elements. This is particularly useful when dynamically updating the UI in response to user actions or server responses.
* **Event Handling:**
    * jQuery provides a concise and cross-browser-compatible way to handle events. This is crucial for capturing user interactions like button clicks, input changes, and other events that trigger actions in the application.
* **AJAX Communication:**
    * jQuery simplifies AJAX requests, making it easier to communicate with the server asynchronously. In this code, AJAX is used to perform actions like deleting trades, fetching trade details, and saving trades without requiring a full page reload.
* **Form Handling:**
    * jQuery facilitates form handling, especially in conjunction with AJAX. It helps in managing form visibility, handling form submissions, and dynamically updating form elements based on user input.
* **Real-time Calculations:**
    * The code involves real-time calculations based on user input. jQuery, combined with event listeners, allows for efficient handling of user input changes and triggers the recalculation of trade values without the need for a page refresh.
* **Cross-browser Compatibility:**
    * jQuery abstracts away many of the cross-browser compatibility issues, ensuring that the code behaves consistently across different web browsers.
* **Code Readability and Conciseness:**
    * jQuery provides a concise syntax for common tasks, resulting in more readable and maintainable code compared to raw JavaScript. This is especially beneficial when dealing with complex interactions and manipulations.
* **Asynchronous User Experience:**
    * The use of AJAX in combination with jQuery contributes to an asynchronous user experience. Instead of waiting for full page reloads, users can see real-time updates and interactions, enhancing the overall responsiveness of the application.


#### **Initalisation and Event Listeners**

<code> 
$(document).ready(function () {
    // jQuery code
    // ... (Initialisation of variables and event listeners)
});

</code>

* The code inside the $(document).ready() function ensures that the script runs after the HTML document is fully loaded.


#### **Trade Deletetion**

<code> 
// Add an event listener for the delete button
$('.delete-trade-button').click(function () {
    // ... (Function to delete a trade using AJAX)
});

</code>

* This code sets up an event listener for the click on a button with the class delete-trade-button. When clicked, it triggers a function to delete a trade using AJAX.

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










