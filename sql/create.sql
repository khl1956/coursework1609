/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     24.11.2019 5:24:59                           */
/*==============================================================*/

drop table if exists Documents;
drop table if exists Fields;
drop table if exists Templates;
drop table if exists Users;

drop sequence if exists documents_document_id_seq;
drop sequence if exists fields_field_id_seq;
drop sequence if exists templates_template_id_seq;
drop sequence if exists users_user_id_seq;

/*==============================================================*/
/* Table: Documents                                             */
/*==============================================================*/
create table Documents (
   document_id          SERIAL                 not null,
   user_id              INT4                 null,
   document_name        TEXT         not null,
   document_file_path   TEXT         not null,
   document_upload_date DATE                 null,
   constraint PK_DOCUMENTS primary key (document_id)
);

/*==============================================================*/
/* Table: Fields                                                */
/*==============================================================*/
create table Fields (
   field_id             SERIAL                 not null,
   template_id          INT4                 null,
   field_name           TEXT         not null,
   field_content        TEXT                 not null,
   constraint PK_FIELDS primary key (field_id)
);

/*==============================================================*/
/* Table: Templates                                             */
/*==============================================================*/
create table Templates (
   template_id          SERIAL                 not null,
   user_id              INT4                 null,
   template_name        TEXT         not null,
   template_file_path   TEXT         not null,
   template_upload_date DATE                 not null,
   constraint PK_TEMPLATES primary key (template_id)
);

/*==============================================================*/
/* Table: Users                                                 */
/*==============================================================*/
create table Users (
   user_id              SERIAL                 not null,
   password_hash        TEXT          not null,
   username             TEXT          not null,
   email                TEXT         not null,
   constraint PK_USERS primary key (user_id)
);

alter table Documents
   add constraint FK_DOCUMENT_USER_DOCU_USERS foreign key (user_id)
      references Users (user_id)
      on delete cascade on update cascade;

alter table Fields
   add constraint FK_FIELDS_TEMPLATE__TEMPLATE foreign key (template_id)
      references Templates (template_id)
      on delete cascade on update cascade;

alter table Templates
   add constraint FK_TEMPLATE_USER_TEMP_USERS foreign key (user_id)
      references Users (user_id)
      on delete cascade on update cascade;

