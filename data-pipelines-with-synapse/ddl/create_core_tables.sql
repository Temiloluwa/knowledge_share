-- Check if the table exists
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ProjectDimension')
BEGIN
    -- Create the ProjectDimension table
    CREATE TABLE ProjectDimension (
        ProjectKey INT PRIMARY KEY,
        ProjectName NVARCHAR(255),
        ProjectStart DATE,
        ProjectEnd DATE,
        RevenueGenerated MONEY
    );

    -- Insert sample data
    END

----

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DeveloperDimension')
BEGIN

 CREATE TABLE DeveloperDimension (
        DeveloperKey INT PRIMARY KEY,
        DeveloperName NVARCHAR(255),
        DeveloperRole NVARCHAR(100)
    );
