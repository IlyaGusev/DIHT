ATTACH DATABASE "fivt2ka.db" AS old;
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined from old.auth_user;
INSERT INTO accounts_profile (id, user_id, sex, hostel, room_number, group_number, money, mobile, middle_name)
SELECT id, user_id, sex, hostel, room_number, group_number, money, mobile, middle_name from old.accounts_userprofile;
