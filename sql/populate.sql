insert into Users(password_hash, username, email) values('0fdbd0e198456d182fa75185a4f31e89f237a32d86b03e0bdea486b5294f92b8', 'eugen1344', 'eu@gmail.com');
insert into Users(password_hash, username, email) values('18c08049d608a1bcea25c20c1dcc0ff35edb3c1460d2fd41fd9eaab4bb7f6b1a', 'eugen1334', 'eu1@gmail.com');
insert into Users(password_hash, username, email) values('14cc3e6019f4eac5c1316ce630d9a8d3e497693a9ddf1a0eb3ccca7072c669df', 'eugen1434', 'eu2@gmail.com');

insert into Documents(user_id, document_name, document_file_path, document_upload_date) values(1, 'CV', '/eugen1344/CV.doc', to_date('01011897','DDMMYYYY'));
insert into Documents(user_id, document_name, document_file_path, document_upload_date) values(1, 'CV', '/eugen1344/CV — копия.doc', to_date('01011899','DDMMYYYY'));
insert into Documents(user_id, document_name, document_file_path, document_upload_date) values(1, 'CV', '/eugen1344/CV — копия — копия.doc', to_date('01011898','DDMMYYYY'));

insert into Templates(user_id, template_name, template_file_path, template_upload_date) values(1, 'CV', '/eugen1344/CV.tex', to_date('01011890','DDMMYYYY'));
insert into Templates(user_id, template_name, template_file_path, template_upload_date) values(2, 'Song', '/eugen1344/Song.tex', to_date('01012005','DDMMYYYY'));
insert into Templates(user_id, template_name, template_file_path, template_upload_date) values(3, 'Laboratory_Physics', '/eugen1344/Laboratory_Physics.tex', to_date('01012011','DDMMYYYY'));

insert into Fields(template_id, field_name, field_content) values(1, 'name', 'Evgeniy');
insert into Fields(template_id, field_name, field_content) values(1, 'phone', '88005553535');
insert into Fields(template_id, field_name, field_content) values(1, 'github_link', 'https://github.com/eugen1344');