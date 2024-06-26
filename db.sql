CREATE SCHEMA ODATA;

CREATE COLUMN TABLE ODATA.PRODUCTS(
	ProductID INT PRIMARY KEY,
	ProductName CHAR(100) NOT NULL,
	SupplierID CHAR(3) NOT NULL,
	CategoryID CHAR(3) NOT NULL,
	QuantityPerUnit CHAR(40) NOT NULL,
	UnitPrice CHAR(10) NOT NULL,
	UnitsInStock CHAR(3) NOT NULL,
	UnitsOnOrder CHAR(3) NOT NULL,
	ReorderLevel CHAR(3) NOT NULL,
	Discontinued CHAR(5) NOT NULL
);