Project Theme:	
	ECommerceOrderManagementSystem
	E-Commerce Order Management System 	Model user roles (buyer, seller, admin), 
	login and payment validation, 
	product filtering, and dynamic discount logic.

Tech Skills:
  FE: HTML(Bootstrap),JavaScript(JQuery)
  BE: Python(fastAPI, sqlalchemy)
  DB: SQLite

Stories, Scenarioes and sub-tasks:
  [Story1] Story: User(buyer) registration and Login
  	[Story1] Acceptance Criteria(Scenarios):
  		Scenario 1: User(buyer) registration
  		Scenario 2: User(buyer) login
  	[Story1] Sub-tasks: 
  		1. [FE] User(Buyer) registration UI.
  		2. [FE] User(Buyer) registration username, password, email and mobile pone validation, user registration.
  		3. [BE] User(Buyer) registration API and repeating users(username, email, mobile phone) checking
  		4. [FE] User(Buyer) login UI.
  		5. [FE] User(Buyer) login username and password validation, user login.
  		6. [BE] User(Buyer) login API, repeating users(username, email, mobile phone) validation.
  
  [Story2] Story: Displaying and filtering products
  [Story2] Acceptance Criteria(Scenarios):
    Scenario 1: Displaying and filtering products
    Scenario 2: Showing product’s discount price
  [Story2] Sub-tasks: 
    1. [FE] products UI.
    2. [FE] Displaying and filtering products.
    3. [BE] Displaying and filtering products API.
    4. [FE] Displaying product’s discount price.
    5. [BE] Displaying product’s discount price API.
    6. [BE] User(Buyer) permission validation for Displaying and filtering products API, Displaying product’s discount price API.
  
  [Story3] Story: Adding products to cart and payment
  [Story3] Acceptance Criteria(Scenarios):
    Scenario 1: Adding products to the shopping cart
    Scenario 2: Displaying products in the shopping cart
    Scenario 3: Payment and validation
  [Story3] Sub-tasks: 
    1. [FE] shopping cart UI.
    2. [BE] Counting products in shopping cart API.
    3. [FE] Displaying products in shopping cart UI.
    4. [BE] Product list of shopping cart API.
    4. [FE] Deleting products from shopping cart.
    5. [BE] Deleting products from shopping cart API.
    6. [FE] Payment and validation.
    7. [BE] Payment API and validation.
    8. [BE] User(Buyer) permission validation for Counting products in shopping cart API, Deleting products from shopping cart API, Payment API.
  
  [Story4] Story: User(Seller) login and products management
  [Story4] Acceptance Criteria(Scenarios):
    Scenario 1: User(Seller) login
    Scenario 2: Products management
    Scenario 3: Inventory management	
  [Story4] Sub-tasks: 
    1. [FE] User(Seller) login UI.
    2. [FE] User’s(Seller) username, password validation and login validation.
    3. [BE] User’s(Seller) username, password validation and login API.
    4. [FE] Products management UI.
    5. [BE] Products API.
    6. [FE] Creating products UI.
    7. [BE] Creating products API.
    8. [FE] Deleting products.
    9. [BE] Deleting products API.
    10. [FE] Inventory management UI.
    11. [FE] Changing(Increasing and decreasing) Inventory.
    12. [FE] Changing(Increasing and decreasing) Inventory API.
    13. [BE] User(Seller) permission validation for Creating products API, Deleting products API, Changing Inventory API.
  
  
  [Story5] Story: Discount management
  [Story5] Acceptance Criteria(Scenarios):
    Scenario 1: Discount management
  [Story5] Sub-tasks: 
    1. [FE] Displaying product’s discount UI.
    2. [FE] Displaying product’s discount.
    3. [BE] Displaying product’s discount API.
    4. [FE] Creating product’s discount.
    5. [BE] Creating product’s discount API.
    6. [FE] Deleting product’s discount.
    7. [BE] Deleting product’s discount API.
    8. [BE] User(Seller) permission validation for Displaying product’s discount API, Creating product’s discount API, Deleting product’s discount API.
  
  [Story6] Story: User(Admin) login and users management
  [Story6] Acceptance Criteria(Scenarios):
    Scenario 1: User(Admin) login
    Scenario 2: Users management
    Scenario 3: Create users(Seller)
  [Story6] Sub-tasks: 
    1. [FE] User(Admin) login UI.
    2. [FE] User’s(Admin) username, password validation and login validation.
    3. [BE] User’s(Admin) username, password validation and login API.
    4. [FE] Displaying users UI.
    5. [FE] Users management(disabled, enabled).
    6. [BE] Users management(disabled, enabled) API.
    7. [FE] Creating users(Seller).
    8. [BE] Creating users(Seller) API.
    9. [BE] User(Admin) permission validation for Users management API, Creating users(Seller) API.
