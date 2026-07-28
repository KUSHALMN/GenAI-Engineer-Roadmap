-- Update a user's age by id
UPDATE users
SET age = 23
WHERE id = 1;

-- Update multiple fields
UPDATE users
SET name = 'Kushal MN', email = 'kushalmn@example.com'
WHERE id = 1;
