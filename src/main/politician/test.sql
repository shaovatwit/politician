-- INSERT INTO Politicians_Politician (politician_id, name, gov_link, campaign_link, email, phone, address, party, date_elected, biography, district)
-- VALUES (1, 'John Doe', 'asdf.com', 'johncampaign.com', 'johndoe@gmail.com', '800-800-8000', '1 Beale St', 'Democrat', '09-13-2023', 'Wada', 'Wala');
INSERT INTO Politicians_Politician (politician_id, name, gov_link, campaign_link)
VALUES (2, 'Ed Flynn', 'https://www.boston.gov/departments/city-council/ed-flynn', 'https://www.edforboston.com/');
-- INSERT INTO Politicians_City (city_id, name, state, politician_id) VALUES (1, 'Boston', 'MA', 1);

-- psql -d Politician -c "TRUNCATE Politicians_City CASCADE; TRUNCATE Politicians_Department CASCADE; TRUNCATE Politicians_Politician CASCADE;"